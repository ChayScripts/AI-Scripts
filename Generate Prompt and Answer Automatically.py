# Install ollama and pull any model. 
# Install Python. Below script is tested on Python 3.13.3 version.
# Finally run below script on a terminal on the server. 

import requests
import os

# ==== CONFIGURATION ====
USE_OPENAI = False  # Set to True if using OpenAI
OPENAI_API_KEY = "your-openai-key"
API_BASE_URL = "http://localhost:11434/api/generate"  # Corrected for Ollama
MODEL_NAME = "qwen3:8b"  # Change as needed

# ==== CORE FUNCTION ====
def ask_model(messages):
    headers = {"Content-Type": "application/json"}

    if USE_OPENAI:
        url = "https://api.openai.com/v1/chat/completions"
        headers["Authorization"] = f"Bearer {OPENAI_API_KEY}"
        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": 0.7,
        }
    else:
        url = API_BASE_URL
        # Flatten messages into a prompt string for Ollama
        prompt = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["response"] if not USE_OPENAI else response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] Failed request to: {url}\n{e}\n")
        exit(1)
    except ValueError as e:
        print(f"\n[ERROR] Failed to parse response JSON from: {url}\n{e}\n")
        print("Raw response:", response.text)
        exit(1)

# ==== AUTOMATED FUNCTION ====
def auto_prompt_engineer(topic):
    system_prompt = {
        "role": "system",
        "content": "You are a helpful assistant that rewrites topics into highly structured, detailed prompts and then answers them completely."
    }
    user_input = {
        "role": "user",
        "content": f"I want to explore the topic: {topic}. First, create a well-structured, specific prompt about it. Then, write the full article based on that prompt directly."
    }

    full_response = ask_model([system_prompt, user_input])
    print("\n[Prompt + Answer]:\n", full_response.strip())

# ==== RUN ====
if __name__ == "__main__":
    topic = input("Enter topic: ").strip()
    auto_prompt_engineer(topic)
