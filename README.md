# 📄 Talk to your PDF

![talk-to-pdf](https://img.shields.io/badge/Status-Prototype-blue?style=for-the-badge)
![python](https://img.shields.io/badge/Python-3.10%2B-green?style=for-the-badge)
![cohere](https://img.shields.io/badge/LLM-Cohere-orange?style=for-the-badge)

A fast and simple Retrieval-Augmented Generation (RAG) app: upload a PDF, ingest content into a local vector database, and ask natural-language questions in a chat interface. All answers are sourced from the uploaded document.

---

## ✨ Features

- Upload PDF file(s) and extract text with `pdfplumber`
- Chunking + embeddings via Cohere `embed-english-v3.0`
- Local persistent vector store: ChromaDB
- Question answering powered by Cohere `command-r-plus`
- Streamlit UI with live chat experience
- Context retention for more accurate follow-ups

---

## 🚀 Quick Start

1. Clone the project

```bash
git clone https://github.com/The-Yesh21/talk-to-pdf.git
cd talk-to-pdf
```

2. Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS / Linux
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Add your Cohere API key

Create `.env` (or edit existing):

```ini
COHERE_API_KEY=your_cohere_api_key_here
```

5. Start the app

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🧪 Usage

- Upload a PDF in the sidebar.
- Wait for successful ingestion and embeddings to create.
- Enter a question; responses are pulled from the source text.
- Upload a new PDF to change context.

---

## 🗂️ Project Structure

```
app.py          # Streamlit UI
ingest.py       # PDF parsing + chunking + embedding + storage
retriever.py    # vector search and retrieval
llm.py          # context prompt to Cohere LLM
requirements.txt
README.md
.env           # Cohere key (never commit)
chroma_db/     # persistent local vector store
```

---

## 🧩 Environment variables

- `COHERE_API_KEY`

Optionally (if you add support later):
- `COHERE_EMBED_MODEL` (default `embed-english-v3.0`)
- `COHERE_LLM_MODEL` (default `command-r-plus`)

---

## 🛠️ Helpful Commands

- Rebuild environment:

```bash
pip install -U -r requirements.txt
```

- Reset vector database (delete `chroma_db/` folder)

- Check ingestion state via logs in the Streamlit UI

---

## 📌 Notes

- Keep files under ~100 MB for best performance.
- Cohere API usage may incur cost; monitor your account.
- No private data is sent to external sources except Cohere API.

---

## 🌱 Roadmap

- Add document search by page number + PDF preview
- Multi-document context blending and conversation history
- Better error handling and metrics

---

## ❤️ Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/name`
3. Commit changes
4. Open a PR

---

## 📄 License

MIT

