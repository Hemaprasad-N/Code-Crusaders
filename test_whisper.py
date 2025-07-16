from app.whisper_handler import transcribe_audio

result = transcribe_audio("input.wav")
print("Whisper Output:", result)