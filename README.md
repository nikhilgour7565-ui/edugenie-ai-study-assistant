# 🎓 EduGenie: Google Gemini Powered Learning Assistant

EduGenie is an interactive, multi-module study companion designed to enhance personalized learning using Google's state-of-the-art **Gemini Large Language Models** (`gemini-1.5-flash`, `gemini-1.5-pro`, `gemini-2.0-flash-exp`), **Streamlit**, **PyPDF**, and **gTTS**.

---

## 🚀 Key Modules & Capabilities

1. 🎓 **Adaptive Concept Explainer & Multimodal Tutor:**
   - Calibrated explanations across 4 audience tiers (*ELI5*, *High School*, *Undergraduate*, *Professional*).
   - Ingests textbook pages, diagrams (`.png`, `.jpg`), and PDFs (`.pdf`).
   - 🔊 Built-in **Text-to-Speech (TTS)** for auditory learning.
   - Multi-format exports: Markdown (`.md`), Plain Text (`.txt`), and Printable HTML (`.html`).

2. ❓ **Smart Quiz & Flashcard Generator:**
   - Dynamic Multiple-Choice Questions (MCQs) with automatic grading, visual score meters (`st.progress`), and explanations.
   - 2-sided active recall flashcards with question front & answer back.

3. 📝 **Multimodal Notes Summarizer & Cheat-Sheet:**
   - Digests lecture transcripts, articles, or uploaded documents up to 12,000+ characters.
   - Extracts Executive Overviews, Key Glossaries, Structured Notes, and 1-Page Exam Cheat Sheets.
   - Audio recap synthesis and multi-format file download.

4. 💬 **Instant Socratic Doubt Clarifier:**
   - 24/7 personalized AI tutor interface using `st.chat_message` with persistent multi-turn conversational context and quick suggestion chips.

---

## 🛠️ Project Structure

```
.
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies (Streamlit, Gemini, PyPDF, gTTS, Pillow)
├── test_app.py                 # Automated unit test suite
├── PROJECT_REPORT.md           # Engineering, architecture & evaluation report
├── .env.example                # Environment variable template
├── .gitignore                  # Git exclusion rules
├── .streamlit/
│   ├── config.toml             # Custom theme & server configuration
│   └── secrets.toml.example    # Cloud secrets configuration example
└── README.md                   # Setup, verification & deployment guide
```

---

## 📦 Local Installation & Setup

### 1. Prerequisites
- Python 3.9+ installed on your system.
- A **Google Gemini API Key** (Obtain a free key from [Google AI Studio](https://aistudio.google.com/app/apikey)).

### 2. Clone or Navigate to Directory
```bash
cd "TN SKILL PROJECT"
```

### 3. Create & Activate Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure API Key
Create a `.env` file in the root folder or copy from `.env.example`:
```bash
cp .env.example .env
```
Open `.env` and add your key:
```env
GEMINI_API_KEY=AIzaSyYourActualAPIKeyHere
```

### 6. Run Automated Tests
```bash
python3 -m unittest test_app.py
```

### 7. Run the Application
```bash
streamlit run app.py
```

The app will launch in your default browser at `http://localhost:8501`.

---

## 🌐 Deploying to Streamlit Community Cloud

1. Push your repository to **GitHub**.
2. Go to [share.streamlit.io](https://share.streamlit.io) and log in with GitHub.
3. Click **"New App"** and select:
   - **Repository:** `your-username/your-repo`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Under **Advanced Settings** -> **Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_api_key"
   ```
5. Click **Deploy!** Streamlit Cloud will automatically install dependencies and launch EduGenie.

---

## 🛡️ Tech Stack
- **Frontend & App Framework:** [Streamlit](https://streamlit.io/)
- **LLM SDK:** [Google GenAI / `google-generativeai`](https://pypi.org/project/google-generativeai/)
- **Configuration Management:** [`python-dotenv`](https://pypi.org/project/python-dotenv/)
