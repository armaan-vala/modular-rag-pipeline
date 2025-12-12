import os
from typing import List
from src.interfaces import BaseLLM, Document
from src.retriever import Retriever

try:
    from groq import Groq
except ImportError:
    Groq = None

class GroqLLM(BaseLLM):
    """
    Adapter for the Groq API.
    """
    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        self.model = model
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = None
        
        if self.api_key and Groq:
            self.client = Groq(api_key=self.api_key)
        else:
            print("Warning: GROQ_API_KEY not set or library missing. LLM running in MOCK mode.")

    async def generate(self, prompt: str) -> str:
        if not self.client:
            return "Mock response: Groq API key is missing."

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                temperature=0.2, # Low temperature for more factual answers
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error communicating with Groq: {str(e)}"

class AnswerEngine:
    """
    The High-Level Manager. 
    It combines the Retriever and the LLM to answer questions (RAG).
    """
    def __init__(self):
        self.retriever = Retriever()
        self.llm = GroqLLM()

    def _construct_prompt(self, query: str, context_docs: List[Document]) -> str:
        """
        Builds the prompt with the retrieved context.
        """
        # Join the content of all retrieved docs
        context_text = "\n\n---\n\n".join([doc.content for doc in context_docs])
        
        # Structured Prompt
        system_prompt = f"""You are a helpful AI assistant. Use the following pieces of context to answer the user's question.
If the answer is not in the context, say "I don't have enough information to answer that based on the provided documents."

CONTEXT:
{context_text}

USER QUESTION: 
{query}

ANSWER:
"""
        return system_prompt

    async def answer(self, query: str) -> str:
        """
        End-to-end RAG pipeline: Query -> Retrieve -> Augment -> Generate
        """
        print(f"Analyzing query: {query}...")
        
        # 1. Retrieve relevant documents
        docs = await self.retriever.retrieve(query)
        
        if not docs:
            return "No relevant information found in the knowledge base."

        # 2. Construct the prompt
        prompt = self._construct_prompt(query, docs)
        
        # 3. Generate answer using Groq
        response = await self.llm.generate(prompt)
        
        return response