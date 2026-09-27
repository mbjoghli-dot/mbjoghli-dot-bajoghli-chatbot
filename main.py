import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# ایجاد اپ FastAPI
app = FastAPI(title="Bajoghli Chatbot API")

# تنظیم CORS — اجازه دادن به Todo App
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:4173",
        "https://bajoghli.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# اتصال به OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    default_headers={
        "HTTP-Referer": "https://bajoghli.netlify.app",
        "X-OpenRouter-Title": "Bajoghli Chatbot",
    },
)


# مدل درخواست
class ChatRequest(BaseModel):
    message: str


# مدل پاسخ
class ChatResponse(BaseModel):
    reply: str


# Endpoint اصلی چت
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="پیام نمی‌تواند خالی باشد")

    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "system",
                    "content": "شما یک دستیار مفید فارسی‌زبان هستید. کوتاه و دقیق پاسخ بده.",
                },
                {"role": "user", "content": request.message},
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        reply = response.choices[0].message.content
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطا در ارتباط با AI: {str(e)}")


# Endpoint سلامت (برای تست)
@app.get("/")
async def root():
    return {"status": "ok", "message": "Bajoghli Chatbot API is running"}