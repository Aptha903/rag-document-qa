RAG Document Q&A Study Assistant

An AI-powered document question-answering application that allows users to upload PDF documents and ask questions based on their content.

The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents and generate context-aware answers using a Large Language Model (LLM).

Instead of searching through lengthy PDF documents manually, users can ask questions and receive answers along with source references, including document names and page numbers.

Features

- PDF Upload: Upload PDF documents through the web interface.
- Document Processing: Extract and divide document content into smaller text chunks.
- Semantic Search: Generate embeddings using Sentence Transformers.
- Vector Search: Store and retrieve relevant text chunks using FAISS.
- AI-Powered Answers: Use the Groq LLM API to generate answers based on retrieved document content.
- Source References: Display the source PDF filename and page number for retrieved information.
- Retrieved Context: Display the relevant passages retrieved from the uploaded documents.
- Context-Based Responses: Answer questions using the available document context rather than relying on unrelated information.

Technologies Used

Technology| Purpose
Python| Backend development and document processing
FastAPI| Building REST API endpoints
FAISS| Vector storage and similarity search
Sentence Transformers| Generating text embeddings
Groq LLM API| Generating natural-language answers
Streamlit| Python-based application interface
HTML| Frontend structure
CSS| Frontend styling
JavaScript| Frontend interactions and API communication

How It Works

The application follows a Retrieval-Augmented Generation (RAG) workflow.

1. PDF Upload: The user uploads a PDF document.
2. Text Extraction: The application extracts text and divides it into smaller chunks.
3. Embedding Generation: Sentence Transformers converts the text chunks into numerical embeddings.
4. Vector Storage: FAISS stores the embeddings for efficient similarity search.
5. Question Processing: The user enters a question through the frontend.
6. Information Retrieval: The question is converted into an embedding, and FAISS retrieves relevant document passages.
7. Answer Generation: The retrieved passages are provided as context to the Groq LLM API.
8. Response Display: The application displays the generated answer, source references, and retrieved passages.

Project Structure

rag-document-qa/
│
├── frontend/
│   ├── index.html          # Frontend structure
│   ├── style.css           # Frontend styling
│   └── script.js           # Frontend logic and API calls
│
├── api.py                  # FastAPI backend and API endpoints
├── app.py                  # Streamlit application
├── ingest.py               # PDF processing and document ingestion
├── search.py               # Document retrieval and vector search
├── rank.py                 # Ranking-related functionality
│
├── chunks.json             # Stored document chunks and metadata
├── index.faiss             # FAISS vector index
├── requirements.txt        # Python dependencies
├── .env                    # API credentials and configuration
└── README.md               # Project documentation

Note: The ".env" file contains API credentials and should not be uploaded to GitHub.

Installation and Setup

1. Clone the Repository

git clone YOUR_GITHUB_REPOSITORY_URL

Navigate into the project directory:

cd rag-document-qa

2. Create a Virtual Environment

python -m venv venv

Activate the environment.

Windows:

venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Configure Environment Variables

Create a ".env" file in the project root directory and add your Groq API key using the environment variable name expected by your application.

GROQ_API_KEY=your_groq_api_key

Do not share or commit your actual API key.

Running the Application

1. Start the FastAPI Backend

From the project root directory, run:

uvicorn api:app --reload

The backend will be available at:

http://127.0.0.1:8000

To explore and test the API endpoints, open:

http://127.0.0.1:8000/docs

2. Start the Frontend

1. Open the "frontend" folder in Visual Studio Code.
2. Open "index.html".
3. Right-click and select Open with Live Server.
4. The application will open in your browser.

Make sure the FastAPI backend is running while using the frontend.

API Endpoints

Method| Endpoint| Description
POST| "/upload"| Upload and process a PDF document
POST| "/ask"| Submit a question and retrieve an answer

The "/ask" endpoint returns:

- "answer" – Generated response.
- "sources" – Source document names, page numbers, and retrieval scores.
- "retrieved_context" – Relevant text passages retrieved from the uploaded documents.

Testing and Evaluation

The application was manually tested using a set of 15 questions to evaluate document-based question answering.

Testing included:

- Asking questions related to uploaded PDF content.
- Checking whether relevant passages were retrieved.
- Verifying generated answers against the document content.
- Checking source filenames and page references.
- Testing questions unrelated to the uploaded document.

An out-of-context question such as "What is the capital of India?" was tested to check whether the application could avoid answering questions unsupported by the uploaded document context.

The application returned an appropriate response indicating that the information was not available in the provided context.

The manually tested questions produced the expected results in the test set. This is an initial functional evaluation and does not represent a guarantee of accuracy for all documents or questions.

Future Improvements

- Support for multiple document formats.
- Improved document retrieval and ranking.
- Chat history and conversational memory.
- More comprehensive automated evaluation.
- Improved handling of ambiguous questions.
- Support for multiple PDF uploads and document collections.

Author

Developed as a personal project to explore Retrieval-Augmented Generation, Large Language Models, semantic search, vector databases, and API-based application development.