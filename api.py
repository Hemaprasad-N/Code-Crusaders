from fastapi import APIRouter, UploadFile, File, HTTPException
from app.whisper_handler import transcribe_audio
from app.translate_handler import translate_ta_to_en
from app.llama_handler import generate_description
from app.db_handler import insert_product, get_all_products
import os
import shutil

router = APIRouter()

@router.post("/process")
async def process_voice(file: UploadFile = File(...)):
    file_location = f"temp_audio_{file.filename}"
    try:
        # Step 0: Save uploaded file temporarily
        try:
            with open(file_location, "wb") as f:
                shutil.copyfileobj(file.file, f)
            print(f"DEBUG: Audio file saved to {file_location}")
        except Exception as e:
            print(f"ERROR: Failed to save uploaded file: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to save audio file: {e}")

        # Step 1: Transcribe Tamil audio
        try:
            original = transcribe_audio(file_location)
            print(f"DEBUG: Transcribed original: {original}")
        except Exception as e:
            print(f"ERROR: Failed to transcribe audio: {e}")
            raise HTTPException(status_code=500, detail=f"Speech-to-Text failed: {e}")

        # Step 2: Translate Tamil ➝ English
        try:
            translated = translate_ta_to_en(original)
            print(f"DEBUG: Translated text: {translated}")
        except Exception as e:
            print(f"ERROR: Failed to translate text: {e}")
            raise HTTPException(status_code=500, detail=f"Translation failed: {e}")

        # Step 3: Generate product description
        try:
            description = generate_description(translated)
            print(f"DEBUG: Generated description: {description}")
        except KeyError as e: # Catch KeyError specifically for the 'response' key
            print(f"ERROR: LLM response missing expected key: {e}. Check llama_handler.py output format.")
            raise HTTPException(status_code=500, detail=f"LLM response format error: Missing key '{e}'.")
        except Exception as e:
            print(f"ERROR: Failed to generate description: {e}")
            raise HTTPException(status_code=500, detail=f"Description generation failed: {e}")

        # Step 4: Store in SQLite DB
        try:
            insert_product(original, translated, description)
            print("DEBUG: Product inserted into DB.")
        except Exception as e:
            print(f"ERROR: Failed to insert product into DB: {e}")
            raise HTTPException(status_code=500, detail=f"Database insertion failed: {e}")

        return {
            "original": original,
            "translated": translated,
            "description": description
        }
    finally:
        # Clean up the temporary file
        if os.path.exists(file_location):
            try:
                os.remove(file_location)
                print(f"DEBUG: Cleaned up temporary file: {file_location}")
            except Exception as e:
                print(f"WARNING: Could not remove temporary file {file_location}: {e}")

@router.get("/products")
async def get_products():
    """
    Retrieves all stored product entries from the database.
    """
    products = get_all_products()
    return {"products": products}

