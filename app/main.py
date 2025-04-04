from fastapi import FastAPI
from app.api.v1.endpoints import chat_router

app = FastAPI()

app.include_router(chat_router, prefix="/api/v1", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Chatbot API"}
