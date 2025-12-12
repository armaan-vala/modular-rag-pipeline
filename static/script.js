const fileInput = document.getElementById('fileInput');
const fileNameDisplay = document.getElementById('fileName');
const statusDiv = document.getElementById('statusMessage');
const chatHistory = document.getElementById('chatHistory');
const queryInput = document.getElementById('queryInput');

// Update filename when file selected
fileInput.addEventListener('change', function() {
    if(this.files && this.files.length > 0) {
        fileNameDisplay.textContent = this.files[0].name;
    }
});

async function uploadFile() {
    if (!fileInput.files.length) {
        showStatus("Please select a file first!", "error");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    showStatus("Uploading & Processing...", "normal");
    
    try {
        const response = await fetch('/ingest', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            showStatus("✅ Ingestion Started! You can chat now.", "success");
        } else {
            showStatus("❌ Upload failed.", "error");
        }
    } catch (error) {
        console.error(error);
        showStatus("❌ Network error.", "error");
    }
}

async function sendQuery() {
    const query = queryInput.value.trim();
    if (!query) return;

    // Add User Message
    addMessage(query, 'user');
    queryInput.value = '';
    
    // Add Loading Message
    const loadingId = addMessage("Thinking...", 'ai');

    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();
        
        // Update AI Message
        document.getElementById(loadingId).querySelector('p').textContent = data.answer;
        
    } catch (error) {
        document.getElementById(loadingId).querySelector('p').textContent = "❌ Error connecting to server.";
    }
}

function addMessage(text, sender) {
    const div = document.createElement('div');
    div.className = `message ${sender}`;
    div.id = `msg-${Date.now()}`;
    div.innerHTML = `<p>${text}</p>`;
    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    return div.id;
}

function showStatus(text, type) {
    statusDiv.textContent = text;
    statusDiv.className = `status ${type}`;
}

function handleEnter(e) {
    if (e.key === 'Enter') sendQuery();
}