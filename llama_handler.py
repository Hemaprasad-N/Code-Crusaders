import requests
import json # Import json module for pretty printing
# No need to import HTTPException here, as we'll raise standard Python exceptions.

def generate_description(prompt: str) -> str:
    """
    Generates a product description using the Ollama Llama2 model.
    Raises standard Python exceptions on error.
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama2",
        "prompt": f"Generate a product description for: {prompt}",
        "stream": False
    }

    try:
        res = requests.post(url, json=payload)
        res.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        response_json = res.json()
        print(f"DEBUG: Full Ollama response JSON:\n{json.dumps(response_json, indent=2)}")

        generated_text = None
        # Attempt to extract the description from common Ollama response keys.
        if "response" in response_json:
            generated_text = response_json["response"]
        elif "content" in response_json:
            generated_text = response_json["content"]
        elif "message" in response_json and "content" in response_json["message"]:
            generated_text = response_json["message"]["content"]
        else:
            # If none of the expected keys are found, raise a KeyError
            raise KeyError("Neither 'response', 'content', nor 'message.content' found in Ollama JSON response.")

        # Validate that the extracted text is a non-empty string
        if not isinstance(generated_text, str) or not generated_text.strip():
            raise ValueError(f"Ollama returned non-string or empty content. Type: {type(generated_text)}, Value: '{generated_text}'")

        return generated_text.strip()

    except requests.exceptions.ConnectionError as e:
        print(f"ERROR: Could not connect to Ollama server at {url}. Is Ollama running?")
        print(f"Error details: {e}")
        raise ConnectionError(f"Failed to connect to Ollama server. Please ensure Ollama is running at {url} and the 'llama2' model is downloaded.") from e
    except requests.exceptions.HTTPError as e:
        print(f"ERROR: HTTP error from Ollama server: {e}")
        print(f"Response content: {res.text}")
        raise RuntimeError(f"Ollama API HTTP error ({e.response.status_code}): {e.response.text}") from e
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to decode JSON from Ollama response: {e}")
        print(f"Raw response text: {res.text}")
        raise ValueError(f"Ollama response was not valid JSON: {e}") from e
    except KeyError as e:
        print(f"ERROR: Missing expected key in Ollama response: {e}")
        raise KeyError(f"Ollama response missing expected key: {e}. Full response: {response_json}") from e
    except ValueError as e: # Catch the new ValueError for content validation
        print(f"ERROR: Ollama content validation failed: {e}")
        raise ValueError(f"Ollama generated invalid or empty content: {e}") from e
    except Exception as e:
        print(f"ERROR: An unexpected error occurred in generate_description: {e}")
        raise RuntimeError(f"An unexpected error occurred during description generation: {e}") from e

