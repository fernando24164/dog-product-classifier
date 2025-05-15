import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic_ai import Agent
from pydantic_ai.providers.groq import GroqProvider

from .routers import classifier, health

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500, detail="GROQ_API_KEY not found in .env file"
        )

    app.state.groq_provider = GroqProvider(api_key=api_key)
    app.state.classifier_agent = Agent(
        "groq:llama-3.1-8b-instant",
        provider=app.state.groq_provider,
        system_prompt="""  
        You are a dog product classification expert. Your task is to classify dog products into the most appropriate category.  
        Analyze the product name and description carefully to determine the best category.  
        Provide a confidence score between 0 and 1, where 1 is the highest confidence.  
        Also suggest relevant subcategories for the product.  
        """,
    )

    yield

    app.state.groq_provider = None
    app.state.classifier_agent = None


def get_application():
    return FastAPI(title="Dog Product Classifier API", lifespan=lifespan)


app = get_application()

app.include_router(classifier.router)
app.include_router(health.router)
