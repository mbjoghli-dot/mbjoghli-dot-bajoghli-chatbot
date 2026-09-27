import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
    default_headers={
        "HTTP-Referer": "http://localhost:3000",
        "X-OpenRouter-Title": "My Chatbot"
    }
)

def chat_with_ai(user_message):
    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {"role": "system", "content": "شما یک دستیار مفید فارسی‌زبان هستید."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"خطا: {e}"

if __name__ == "__main__":
    print("چت‌بات هوش مصنوعی (برای خروج 'exit' بنویسید)")
    while True:
        user_input = input("\nشما: ")
        if user_input.lower() == "exit":
            break
        reply = chat_with_ai(user_input)
        print(f"\nدستیار: {reply}")


