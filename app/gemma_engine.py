import requests

def get_gemma_response(question: str) -> str:
    """
    Sends the user's question to the locally running Ollama Gemma model and returns the response.
    """

    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "gemma3:1b", #gemma3:4b
        "prompt": question,
        "stream": False
    }

    try:
        print("Sending request to Ollama...")  # NEW: debug print
        response = requests.post(url, json=payload, headers=headers, timeout=90)  # NEW: 30s timeout
        response.raise_for_status()
        result = response.json()
        print("Received response from Ollama.")  # NEW: debug print
        return result.get("response", "[No response from Gemma]")
    except Exception as e:
        print(f"Error from Ollama: {e}")  # NEW: error print
        return f"[Error communicating with Gemma via Ollama: {str(e)}]"
