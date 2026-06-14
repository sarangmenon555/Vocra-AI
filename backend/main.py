from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langdetect import detect
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = FastAPI(title="VocraAI — Tamil NLP API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)

LANG_NAMES = {
    "en": "English",
    "ta": "Tamil",
}


class TranslateRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str


class AnalyzeRequest(BaseModel):
    text: str
    task: str


class DetectRequest(BaseModel):
    text: str


def groq_complete(prompt: str, max_tokens: int = 1000) -> str:
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()


@app.get("/")
def root():
    return {"status": "VocraAI API running"}


@app.post("/detect")
def detect_language(req: DetectRequest):
    try:
        detected = detect(req.text)
        lang_name = LANG_NAMES.get(detected, detected)
        return {"detected": detected, "language_name": lang_name}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/translate")
def translate(req: TranslateRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Empty input text")
    if (req.source_lang, req.target_lang) not in [("en", "ta"), ("ta", "en")]:
        raise HTTPException(status_code=400, detail="Only English↔Tamil supported")

    if req.source_lang == "en" and req.target_lang == "ta":
        prompt = f"""Translate the following English text to Tamil script (தமிழ்).
Output ONLY the Tamil translation, nothing else. No explanation, no romanization, no extra text.

English: {req.text}
Tamil:"""
    else:
        prompt = f"""Translate the following Tamil text to English.
Output ONLY the English translation, nothing else. No explanation, no extra text.

Tamil: {req.text}
English:"""

    translated = groq_complete(prompt, max_tokens=512)
    return {
        "original": req.text,
        "translated": translated,
        "source": LANG_NAMES.get(req.source_lang, req.source_lang),
        "target": LANG_NAMES.get(req.target_lang, req.target_lang),
    }


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Empty input text")

    task_prompts = {
        "sentiment": f"""You are a linguistic analysis expert specializing in Tamil and Dravidian languages.
Analyze the sentiment of the following text. If the text is in Tamil script, transliterate key phrases.
Return a JSON object with these fields:
- sentiment: "positive", "negative", or "neutral"
- confidence: a float between 0 and 1
- explanation: 2-3 sentence explanation of the sentiment and any culturally specific nuances
- key_phrases: list of up to 3 key phrases that influenced the sentiment

Text: {req.text}

Respond ONLY with valid JSON, no markdown, no extra text.""",

        "linguistic": f"""You are a Tamil linguistics expert with deep knowledge of Dravidian language morphology.
Analyze the following text and provide linguistic insights.
If it contains Tamil, analyze its structure. If it's in another language, note connections to Tamil where relevant.

Return a JSON object with:
- script_analysis: what script/language is detected
- morphology: 2-3 sentences on word structure, agglutination, or notable grammatical features
- etymology: 1-2 interesting etymological notes if Tamil is present
- complexity_score: integer from 1-10 indicating linguistic complexity
- fun_fact: one fascinating fact about Tamil related to the text's content or structure

Text: {req.text}

Respond ONLY with valid JSON, no markdown, no extra text.""",

        "summarize": f"""You are an expert in Tamil and Indian languages.
Summarize the following text concisely. If the text is in Tamil, provide the summary in both Tamil and English.
If in another language, provide summary in that language and English.

Return a JSON object with:
- summary_english: concise English summary (2-4 sentences)
- summary_original: summary in the original language (2-4 sentences)
- key_points: list of 3-5 key bullet points in English
- word_count: approximate word count of original

Text: {req.text}

Respond ONLY with valid JSON, no markdown, no extra text.""",

        "transliterate": f"""You are an expert in Tamil script and romanization.
Transliterate the following Tamil text to Roman script using standard Tamil romanization.
If the text is already in Roman script, convert it to Tamil script.

Return a JSON object with:
- original: the original text
- transliterated: the converted text
- pronunciation_guide: a simple pronunciation guide for non-Tamil speakers
- script_direction: "Tamil to Roman" or "Roman to Tamil"

Text: {req.text}

Respond ONLY with valid JSON, no markdown, no extra text.""",
    }

    if req.task not in task_prompts:
        raise HTTPException(status_code=400, detail=f"Unknown task: {req.task}")

    raw = groq_complete(task_prompts[req.task])
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {"raw_output": raw}

    return {"task": req.task, "result": result}


@app.get("/languages")
def get_languages():
    return {"languages": LANG_NAMES}