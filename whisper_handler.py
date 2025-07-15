import whisper

model = whisper.load_model("base")

def transcribe_audio(audio_path="input.wav", language="ta"):
    result = model.transcribe(audio_path, language=language)
    return result["text"]
