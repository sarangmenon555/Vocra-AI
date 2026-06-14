# TamilBridge — தமிழ் பாலம்

**NLP tooling for one of humanity's oldest living languages.**

Tamil is not merely old — it is ancient in a way almost no living language can claim. With a continuous literary tradition stretching back over 2,500 years, Tamil predates the arrival of Sanskrit in South India and stands as one of the few classical languages whose unbroken literary heritage has survived into the modern era. The Sangam literature of the 3rd century BCE remains readable by educated Tamil speakers today — a testament to the language's extraordinary stability and cultural continuity. Tamil is the official language of Tamil Nadu (India) and Sri Lanka, spoken by over 80 million people worldwide, and recognized as a classical language by the Government of India.

Yet Tamil, like virtually all Dravidian languages, is dramatically underrepresented in modern NLP systems. Most large language models are trained predominantly on English and a handful of European languages. Tamil speakers have had limited access to high-quality machine translation, sentiment analysis, and linguistic tooling in their own language.

TamilBridge is built to change that.

---

## What it does

**Translation** — High-quality neural machine translation between Tamil and 200+ other languages using Meta's NLLB-200 (No Language Left Behind) model, a system specifically designed to address low-resource language translation.

**Sentiment Analysis** — Detect emotional tone in Tamil text with cultural nuance, backed by Llama 3.3 70B. Outputs sentiment label, confidence score, key phrases, and a linguistically-aware explanation.

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
```

**Backend:**
- FastAPI + Uvicorn
- `facebook/nllb-200-distilled-600M` via HuggingFace Transformers (runs locally, no API cost)
- Groq API with `llama-3.3-70b-versatile` for analysis tasks
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

Add your Groq API key in `main.py`:

```python
GROQ_API_KEY = "your_groq_api_key_here"
```

Start the server:

```bash
uvicorn main:app --reload --port 8000
```

The NLLB-200 model (~2.4GB) will download automatically on first run.

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
| POST | `/translate` | Translate text between supported languages |
| POST | `/analyze` | Run linguistic analysis (sentiment, morphology, summarize, transliterate) |
| POST | `/detect` | Detect language of input text |
| GET | `/languages` | List all supported languages |

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

Tamil (ta), English (en), Hindi (hi), Malayalam (ml), Telugu (te), Kannada (kn), French (fr), German (de), Spanish (es), Arabic (ar), Chinese (zh-cn), and 190+ more via NLLB-200.

---

## Why Tamil

Of the world's 7,000+ languages, fewer than 100 have meaningful NLP tooling. Tamil sits in a peculiar position — large enough in speaker count to deserve attention, classical enough to carry profound cultural weight, yet consistently left behind by the English-first paradigm of most AI research.

The word for "language" in Tamil is மொழி (mozhi). The word for "bridge" — what TamilBridge aspires to be — is பாலம் (palam).

---

## Built for

LingHacks VII — the world's first computational linguistics hackathon for high school students.