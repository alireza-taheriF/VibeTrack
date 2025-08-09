# vibetrack/local_client.py
import requests
import json

API_URL = "http://172.20.10.4:1234/v1/chat/completions"

def send_to_local_model(diff_text: str) -> str:
    messages = [
        {"role": "system", "content": "You are a senior code reviewer. Analyze code diffs."},
        {"role": "user", "content": f"""The following code was changed:

{diff_text}

Please explain:
1. What exactly changed?
2. Why was it changed?
3. What’s the difference in behavior?"""}
    ]

    payload = {
        "model": "mistralai/mathstral-7b-v0.1",  # ← نام دقیق مدل لوکال
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 512
    }

    try:
        response = requests.post(API_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()

        return result["choices"][0]["message"]["content"].strip()

    except requests.exceptions.RequestException as e:
        return f"[❌ Error contacting local model] {str(e)}"

    except KeyError:
        return f"[❌ Invalid response format] {response.text}"
