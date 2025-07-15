from fastapi import APIRouter
from app.whisper_handler import transcribe_audio
from app.translate_handler import translate_ta_to_en
from app.llama_handler import generate_description
from app.db_handler import insert_product

router = APIRouter()

@router.post("/process")
def process_voice():
    original = transcribe_audio()
    translated = translate_ta_to_en(original)
    description = generate_description(translated)
    insert_product(original, translated, description)
    return {
        "original": original,
        "translated": translated,
        "description": description
    }
