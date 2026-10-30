# 📚 AI-Powered Study Assistant (RAG)

An AI-powered study companion that answers questions from PDF study notes using Retrieval-Augmented Generation (RAG). It retrieves relevant information from documents and generates contextual answers with source references.

## ✨ Features

* **PDF Upload:** Add study materials in PDF format.
* **Semantic Search:** Uses Sentence Transformers and FAISS to find relevant document chunks.
* **AI-Powered Answers:** Generates answers using the Groq API.
* **Source References:** Displays source document names and page numbers.
* **Interactive Interface:** Built with Streamlit.
* **REST API:** FastAPI backend for document uploads and question answering.

## 🛠️ Tech Stack

* Python
* FastAPI
* Streamlit
* FAISS
* Sentence Transformers
* Groq API
* PyPDF

## 🏗️ Architecture

1. Upload PDF study notes.
2. Extract and split document text into chunks.
3. Convert chunks into embeddings using Sentence Transformers.
4. Store and search embeddings using FAISS.
5. Retrieve relevant chunks for a user's question.
6. Generate a contextual answer using the Groq API.
7. Display the answer and source references in the Streamlit interface.

## 📁 Project Structure

```text
rag-document-qa/
├── api.py
├── app.py
├── ingest.py
├── search.py
├── list_models.py
├── read_test.py
├── test_llm.py
├── .gitignore
└── README.md
```

## ⚙️ Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/Aptha903/rag-document-qa.git
cd rag-document-qa
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install fastapi uvicorn streamlit requests python-dotenv openai sentence-transformers faiss-cpu numpy pypdf python-multipart
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
LLM_API_KEY=your_groq_api_key
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_MODEL=openai/gpt-oss-20b
```

Replace `your_groq_api_key` with your own Groq API key. Never commit your actual API key to GitHub.

### 5. Prepare the document index

Use the document-ingestion script and the PDF files appropriate for your setup to generate the document chunks and FAISS index. Follow the commands and file paths defined in `ingest.py`.

### 6. Start the FastAPI backend

Open a terminal and run:

```powershell
uvicorn api:app --reload --port 8000
```

API documentation: http://127.0.0.1:8000/docs

### 7. Start the Streamlit application

Open a second terminal in the project folder, activate the virtual environment, and run:

```powershell
python -m streamlit run app.py --server.port 8506
```

Open http://localhost:8506 in your browser.

## 🔐 Security

* API keys are stored in environment variables.
* `.env` and virtual environments are excluded using `.gitignore`.
* Indexed document data is excluded from the repository by default.

## 🚀 Future Improvements

* Support for additional document formats.
* Improved retrieval and answer evaluation.
* Conversation memory and enhanced chat history.
* Deployment to a cloud hosting platform.

## 👩‍💻 Author

**Aptha H P**

GitHub: [Aptha903](https://github.com/Aptha903)

---

RAG Evaluation

The RAG Study Assistant was manually evaluated using 15 test questions based on the uploaded PDF documents.

Evaluation Results

Metric| Result
Total Test Questions| 15
Correctly Retrieved Passages| 15
Incorrect Retrievals| 0
Retrieval Accuracy| 100%

Evaluation Methodology

1. Prepared 15 questions based on the uploaded PDF content.
2. Submitted each question to the RAG chatbot.
3. Examined the retrieved source passages.
4. Verified whether the relevant information was retrieved correctly.
5. Calculated retrieval accuracy based on the results.

Retrieval Accuracy: (15 / 15) × 100 = 100%

Note: This was a manual evaluation using a small test dataset. Performance may vary with different documents and question types.
