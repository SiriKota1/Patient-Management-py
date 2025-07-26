# patient-chatbot-app

Build a Patient Management and Chatbot application using FastAPI, Streamlit, MySQL, and Ollama (LLM).

---

## 🩺 What is this project?

This is a simple CRUD (Create, Read, Update, Delete) API and chatbot application designed for managing patient records while enabling natural language interaction with an integrated LLM (like `llama3.1`) powered by Ollama.

### 🔧 Key Features

- 📝 Add, update, view, and delete patient records (name, record number, blood type, hospital).
- 🤖 Ask health-related or general questions via an LLM.
- 🧠 Saves all chatbot conversations in a MySQL `chat_history` table.
- 📜 Chat history displayed on the sidebar (like ChatGPT-style UI).
- ⚡ FastAPI handles the backend API
- 🎈 Streamlit provides an intuitive web-based UI

---

## 📁 Project Structure
```
patient-chatbot-app/
├── src/
│ ├── patient_chatHistory.py # FastAPI backend (CRUD + chatbot)
├── app_ui.py # Streamlit UI
├── requirements.txt # Python dependencies
└── README.md # Project overview
```
---

## 🚀 Setup & Usage

### 🔹 Step 1: Install dependencies

Make sure you're in a virtual environment (`.venv`), then run:

```bash
pip install -r requirements.txt
ollama run llama3.1
uvicorn src.patient_chatHistory:app --reload
```
### API will be available at: http://127.0.0.1:8000/docs
```
streamlit run app_ui.py
```
