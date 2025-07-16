from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from db_config import get_connection
import httpx

app = FastAPI()


# Allow all CORS (for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model from frontend
class VoiceInput(BaseModel):
    tamil_text: str
    english_translation: str

# Function to call Ollama (LLaMA or Mistral)
async def generate_with_ollama(prompt: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "mistral",  
                    "prompt": prompt,
                    "stream": False
                }
            )
            print("🧠 Ollama AI Response:", response.status_code)
            print(response.text)
            data = response.json()
            return data.get("response", "AI generation failed.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"AI Error: {str(e)}"

# API endpoint to save voice input and AI-generated text
@app.post("/save-voice")
async def save_voice(input: VoiceInput):
    # Optional filter for irrelevant input
    if "பெயர்" in input.tamil_text:
        return {"message": "Input not a product. Ignored."}

    # Prompt for AI model
    prompt = f"""
    You are a helpful assistant generating descriptions for a rural catalog.
    Write a short 2-line product description for: {input.english_translation}
    """

    ai_description = await generate_with_ollama(prompt)

    # Save to MySQL
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO voice_inputs (tamil_text, english_translation) VALUES (%s, %s)",
        (input.tamil_text, ai_description)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {
        "message": "Saved to catalog",
        "generated_text": ai_description
    }

# API endpoint to get all catalog entries
@app.get("/entries")
def get_entries():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM voice_inputs ORDER BY created_at DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
