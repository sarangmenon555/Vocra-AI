# VocraAI — வோக்ரா

**NLP tooling for one of humanity's oldest living languages.**

Tamil is not merely old — it is ancient in a way almost no living language can claim. With a continuous literary tradition stretching back over 2,500 years, Tamil predates the arrival of Sanskrit in South India and stands as one of the few classical languages whose unbroken literary heritage has survived into the modern era. The Sangam literature of the 3rd century BCE remains readable by educated Tamil speakers today — a testament to the language's extraordinary stability and cultural continuity. Tamil is the official language of Tamil Nadu (India) and Sri Lanka, spoken by over 80 million people worldwide, and recognized as a classical language by the Government of India.

Yet Tamil, like virtually all Dravidian languages, is dramatically underrepresented in modern NLP systems. Most large language models are trained predominantly on English and a handful of European languages. Tamil speakers have had limited access to high-quality machine translation, sentiment analysis, and linguistic tooling in their own language.

VocraAI is built to change that.

---

## What it does

**Translation** — English to Tamil and Tamil to English, powered by Llama 3.3 70B via Groq with prompting tuned specifically for Tamil script output.

**Sentiment Analysis** — Detect emotional tone in Tamil text with cultural nuance. Outputs sentiment label, confidence score, key phrases, and a linguistically-aware explanation.

**Linguistic Analysis** — Deep morphological and etymological analysis of Tamil text. Tamil is an agglutinative language with a highly regular morphological system — suffixes encode tense, mood, person, number, and case in complex but rule-governed ways. This tool surfaces those features.

**Summarization** — Condense long Tamil text into concise summaries in both Tamil and English, with key points extracted.

**Transliteration** — Convert between Tamil script (நன்றி) and Roman transliteration (nandri) with pronunciation guidance for non-Tamil speakers.

**Language Detection** — Automatically identify the language of any input text.

---

## Architecture

```
frontend/index.html     React single-page app, no build step required
backend/main.py         FastAPI REST API
backend/requirements.txt
backend/.env            Your Groq API key (never commit this)
```

**Backend:**
- FastAPI + Uvicorn
- Groq API with `llama-3.3-70b-versatile` for all NLP tasks including translation
- `langdetect` for language identification

**Frontend:**
- React 18 via CDN (no build step)
- Noto Sans Tamil for Tamil script rendering
- Cormorant Garamond + Inter for UI typography

---

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key at https://console.groq.com

Start the server:

```bash
uvicorn main:app --reload --port 8000
```

### Frontend

No build step needed. Open `frontend/index.html` directly in a browser, or serve it:

```bash
cd frontend
python -m http.server 3000
```

Then open `http://localhost:3000`.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/translate` | Translate between English and Tamil |
| POST | `/analyze` | Run linguistic analysis (sentiment, morphology, summarize, transliterate) |
| POST | `/detect` | Detect language of input text |
| GET | `/languages` | List supported languages |

### Example: Translate to Tamil

```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Knowledge is power", "source_lang": "en", "target_lang": "ta"}'
```

### Example: Sentiment Analysis

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "இது மிகவும் அழகான நாள்", "task": "sentiment"}'
```

---

## Supported Languages

English (en) and Tamil (ta) — bidirectional translation and full NLP analysis.

---

## Why Tamil

Of the world's 7,000+ languages, fewer than 100 have meaningful NLP tooling. Tamil sits in a peculiar position — large enough in speaker count to deserve attention, classical enough to carry profound cultural weight, yet consistently left behind by the English-first paradigm of most AI research.

The word for "voice" in Tamil is குரல் (kural). VocraAI takes its name from "vox" (Latin: voice) and "AI" — a voice for Tamil in the age of artificial intelligence.

---

## Built for

LingHacks VII — the world's first computational linguistics hackathon for high school students.