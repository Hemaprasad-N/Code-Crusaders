import requests

def generate_description(prompt):
    res = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama2",
        "prompt": f"Generate a product description for: {prompt}",
        "stream": False
    })
    return res.json()["response"]
