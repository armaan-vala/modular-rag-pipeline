import pytest
import os
from src.interfaces import Document
from src.ingestion import IngestionEngine, TextChunker

# --- Fixtures ---

@pytest.fixture
def temp_txt_file(tmp_path):
    """Creates a temporary text file for testing."""
    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "test_doc.txt"
    p.write_text("This is a sample document used for automated testing of the RAG pipeline.")
    return str(p)

@pytest.fixture
def empty_txt_file(tmp_path):
    """Creates an empty temporary text file."""
    p = tmp_path / "empty.txt"
    p.write_text("")
    return str(p)

@pytest.fixture
def ingestion_engine():
    return IngestionEngine()

@pytest.fixture
def text_chunker():
    return TextChunker(chunk_size=50, chunk_overlap=10)

# --- Tests ---

def test_happy_path_ingestion(ingestion_engine, temp_txt_file):
    """Test 1: Valid Input -> Success"""
    docs = ingestion_engine.load_file(temp_txt_file)
    assert len(docs) == 1
    assert docs[0].metadata['source'] == "test_doc.txt"
    assert "sample document" in docs[0].content

def test_unhappy_path_empty_file(ingestion_engine, empty_txt_file):
    """Test 2: Empty File -> Raises ValueError"""
    # Should raise ValueError because content length < 10
    with pytest.raises(ValueError, match="contained no valid text"):
        ingestion_engine.load_file(empty_txt_file)

def test_chunker_empty_input(text_chunker):
    """Test 3: Empty Input List -> Raises ValueError"""
    with pytest.raises(ValueError, match="Input document list cannot be empty"):
        text_chunker.chunk_documents([])

def test_chunker_logic(text_chunker):
    """Test 4: Verify chunking actually splits text"""
    long_text = "A" * 100 # 100 chars
    doc = Document(content=long_text, metadata={"source": "test", "type": "txt"})
    
    chunks = text_chunker.chunk_documents([doc])
    
    # chunk_size is 50, so we expect roughly 2-3 chunks depending on overlap
    assert len(chunks) >= 2
    assert chunks[0].metadata['chunk_index'] == 0
    assert chunks[1].metadata['chunk_index'] == 1

def test_metadata_validation(ingestion_engine):
    """Test 5: Internal validation logic"""
    # Create a document missing 'source'
    bad_doc = Document(content="Valid content", metadata={"type": "txt"})
    
    with pytest.raises(ValueError, match="missing required metadata keys"):
        ingestion_engine._validate_document(bad_doc)