// ========================================
// API CONFIGURATION
// ========================================

const API_URL = "http://127.0.0.1:8000";


// ========================================
// HTML ELEMENTS
// ========================================

const pdfFile = document.getElementById("pdfFile");
const uploadBtn = document.getElementById("uploadBtn");
const uploadStatus = document.getElementById("uploadStatus");

const chatMessages = document.getElementById("chatMessages");
const questionInput = document.getElementById("questionInput");
const sendBtn = document.getElementById("sendBtn");


// ========================================
// SAFE HTML DISPLAY
// ========================================

function escapeHTML(text) {

    return String(text ?? "").replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    })[char]);

}


// ========================================
// DISPLAY CHAT MESSAGE
// ========================================

function addMessage(content, sender) {

    const message = document.createElement("div");

    message.className = `message ${sender}-message`;

    message.textContent = content;

    chatMessages.appendChild(message);

    chatMessages.scrollTop = chatMessages.scrollHeight;

    return message;

}


// ========================================
// DISPLAY ANSWER AND SOURCES
// ========================================

function displayAnswer(data) {

    const container = document.createElement("div");

    container.className = "message assistant-message";

    let html = `
        <div class="answer-section">

            <h3>💡 Answer</h3>

            <p>${escapeHTML(data.answer)}</p>

        </div>
    `;


    // ====================================
    // SOURCES SECTION
    // ====================================

    if (data.sources && data.sources.length > 0) {

        html += `

            <div class="sources-section">

                <h3>📚 Sources (${data.sources.length})</h3>

                <div class="source-list">

        `;

        data.sources.forEach((source, index) => {

            html += `

                <div class="source-item">

                    <span class="source-number">
                        ${index + 1}
                    </span>

                    <div class="source-details">

                        <strong>
                            ${escapeHTML(source.file)}
                        </strong>

                        <span>
                            Page ${escapeHTML(source.page)}
                        </span>

                    </div>

                </div>

            `;

        });

        html += `

                </div>

            </div>

        `;

    }


    // ====================================
    // RETRIEVED CONTEXT SECTION
    // ====================================

    if (
        data.retrieved_context &&
        data.retrieved_context.length > 0
    ) {

        html += `

            <div class="retrieved-section">

                <h3>🔍 Retrieved Context</h3>

                <p class="section-description">
                    Relevant passages retrieved from your documents.
                </p>

        `;


        data.retrieved_context.forEach((item, index) => {

            html += `

                <div class="retrieved-card">

                    <div class="retrieved-header">

                        <strong>
                            Retrieved Passage ${index + 1}
                        </strong>

                        <span>
                            Page ${escapeHTML(item.page)}
                        </span>

                    </div>


                    <p class="retrieved-text">
                        ${escapeHTML(item.text)}
                    </p>


                    <div class="retrieved-footer">

                        <span>
                            📄 ${escapeHTML(item.file)}
                        </span>

                        <span>
                            Score: ${escapeHTML(item.score)}
                        </span>

                    </div>

                </div>

            `;

        });


        html += `

            </div>

        `;

    }


    // Display complete response

    container.innerHTML = html;

    chatMessages.appendChild(container);

    chatMessages.scrollTop = chatMessages.scrollHeight;

}


// ========================================
// PDF UPLOAD FUNCTION
// ========================================

uploadBtn.addEventListener("click", async () => {

    const file = pdfFile.files[0];


    if (!file) {

        uploadStatus.textContent =
            "Please select a PDF file first.";

        return;

    }


    if (!file.name.toLowerCase().endsWith(".pdf")) {

        uploadStatus.textContent =
            "Only PDF files are supported.";

        return;

    }


    const formData = new FormData();

    formData.append("file", file);


    uploadBtn.disabled = true;

    uploadStatus.textContent =
        "Uploading and processing your PDF...";


    try {

        const response = await fetch(
            `${API_URL}/upload`,
            {
                method: "POST",
                body: formData
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "PDF upload failed."
            );

        }


        uploadStatus.textContent =
            data.message || "PDF uploaded successfully!";


    }

    catch (error) {

        uploadStatus.textContent =
            "Upload error: " + error.message;

    }

    finally {

        uploadBtn.disabled = false;

    }

});


// ========================================
// ASK QUESTION FUNCTION
// ========================================

async function askQuestion() {

    const question = questionInput.value.trim();


    if (!question) {

        return;

    }


    // Remove welcome screen after first question

    const welcomeScreen =
        document.querySelector(".welcome-screen");

    if (welcomeScreen) {

        welcomeScreen.remove();

    }


    // Display user's question

    addMessage(question, "user");

    questionInput.value = "";

    sendBtn.disabled = true;


    // Loading message

    const loadingMessage = addMessage(
        "Searching your documents and generating an answer...",
        "assistant"
    );


    try {

        const response = await fetch(
            `${API_URL}/ask`,
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })

            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "Unable to generate an answer."
            );

        }


        // Remove loading message

        loadingMessage.remove();


        // Display answer, sources and retrieved context

        displayAnswer(data);


    }

    catch (error) {

        loadingMessage.textContent =
            "Sorry, something went wrong: " + error.message;

    }

    finally {

        sendBtn.disabled = false;

        questionInput.focus();

    }

}


// ========================================
// SEND BUTTON
// ========================================

sendBtn.addEventListener("click", askQuestion);


// ========================================
// ENTER KEY TO SEND QUESTION
// ========================================

questionInput.addEventListener("keydown", event => {

    if (event.key === "Enter") {

        event.preventDefault();

        askQuestion();

    }

});