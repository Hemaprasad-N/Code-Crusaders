from transformers import MarianMTModel, MarianTokenizer

model_name = "Helsinki-NLP/opus-mt-ta-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def translate_ta_to_en(text):
    tokens = tokenizer.prepare_seq2seq_batch([text], return_tensors="pt")
    translation = model.generate(**tokens)
    return tokenizer.decode(translation[0], skip_special_tokens=True)
