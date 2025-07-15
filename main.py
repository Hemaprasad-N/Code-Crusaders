from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db_config import get_connection
import httpx

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model
class VoiceInput(BaseModel):
    tamil_text: str
    english_translation: str

# Call LLaMA via Ollama
async def generate_with_llama(prompt: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2",
                "prompt": prompt,
                "stream": False
            }
        )
        data = response.json()
        return data.get("response", "LLaMA failed to generate text.")

# POST endpoint: Save voice input
@app.post("/save-voice")
async def save_voice(input: VoiceInput):
    prompt = f"Write a simple and clear product description in 2-3 sentences for: {input.english_translation}"
    ai_description = await generate_with_llama(prompt)

    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO voice_inputs (tamil_text, english_translation) VALUES (%s, %s)"
    cursor.execute(query, (input.tamil_text, ai_description))
    conn.commit()
    cursor.close()
    conn.close()

    return {
        "message": "Saved with AI-generated text",
        "generated_text": ai_description
    }

# GET endpoint: Show all entries (for dashboard.html)
@app.get("/entries")
def get_all_entries():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM voice_inputs ORDER BY created_at DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
