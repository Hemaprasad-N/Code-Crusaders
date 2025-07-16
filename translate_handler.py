import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

# Determine the device to use (GPU if available, otherwise CPU)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Define the model name on Hugging Face Hub.
# When loading online, this is the identifier for the model.
MODEL_NAME = "facebook/nllb-200-distilled-600M"

print(f"Attempting to load NLLB model '{MODEL_NAME}' online from Hugging Face Hub.")
print("This will download the model the first time it's run, requiring an internet connection.")

# Load the tokenizer and model from the Hugging Face Hub.
# This operation requires an internet connection for the very first run
# to download the model files to your local Hugging Face cache.
# Subsequent runs will load from the cache and be offline-capable.
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(DEVICE)
print(f"Successfully loaded NLLB model '{MODEL_NAME}' on {DEVICE}.")


def translate_ta_to_en(text: str) -> str:
    """
    Translates Tamil text to English using facebook/nllb-200-distilled-600M.
    This function loads the model from Hugging Face Hub (online first-time download).
    """
    # For NLLB models, you specify the source language when tokenizing
    # and the target language when generating.
    # The language codes for NLLB are specific. Tamil is 'tam_Latn', English is 'eng_Latn'.
    # You can find the full list of NLLB language codes here:
    # https://github.com/facebookresearch/fairseq/blob/main/examples/nllb/README.md#language-codes
    source_lang_code = "tam_Latn"
    target_lang_code = "eng_Latn"

    # Set the source language on the tokenizer instance *before* tokenizing.
    # This is the correct way to inform the NLLB tokenizer about the input language.
    tokenizer.src_lang = source_lang_code

    inputs = tokenizer(
        text.strip(),
        return_tensors="pt",
        padding=True,
        truncation=True,
    ).to(DEVICE)

    # Generate the translation, forcing the target language token.
    # For NLLBTokenizerFast, use convert_tokens_to_ids to get the ID for the language token.
    output_ids = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(target_lang_code), # Correct way to get ID for NLLB
        max_length=256
    )

    # Decode the generated token IDs back into a human-readable string.
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

