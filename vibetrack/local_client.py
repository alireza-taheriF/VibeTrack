import requests
import json

API_URL = "http://172.20.10.4:1234/v1/chat/completions"

def send_to_local_model(diff_text, persian_mode=False):
    if persian_mode:
        system_prompt = """تو یک برنامه‌نویس باتجربه و مربی کدنویسی هستی. کارت اینه که تغییرات کد رو به زبان ساده و فارسی توضیح بدی. مخصوصاً برای کسایی که vibe coding میکنن و نمیدونن چی عوض شده."""
        
        user_prompt = f"""این کد تغییر کرده:

{diff_text}

لطفاً به زبان فارسی و ساده توضیح بده:
1. دقیقاً چی عوض شده؟
2. چرا این تغییر انجام شده؟ (احتمالاً چه دلیلی داشته؟)
3. این تغییر چه تأثیری روی رفتار برنامه داره؟
4. اگه کسی ازت سوال بپرسه، چطور میتونی توضیح بدی؟

جوا�� رو به صورت داستانی و قابل فهم بنویس، نه خیلی تکنیکال."""
    else:
        system_prompt = "You are a senior code reviewer and mentor. Analyze code diffs and explain them clearly for developers who might be confused about what changed."
        
        user_prompt = f"""The following code was changed:

{diff_text}

Please explain clearly:
1. What exactly changed?
2. Why was it likely changed? (What was the probable reason?)
3. What's the difference in behavior?
4. How would you explain this to someone who asks about it?

Make your explanation narrative and easy to understand, not overly technical."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    payload = {
        "model": "mistralai/mathstral-7b-v0.1",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        response = requests.post(API_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        if persian_mode:
            return f"❌ خطا در اتصال به هوش مصنوعی: {str(e)}\n\n💡 احتمالاً سرور AI در دسترس نیست. لطفاً تنظیمات رو چک کن."
        else:
            return f"❌ Error connecting to AI: {str(e)}\n\n💡 The AI server might not be available. Please check your configuration."