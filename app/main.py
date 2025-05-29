import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app.routers import products

from .agents.classifier_agent import classifier_agent
from .database.connection import create_db_engine, create_session_factory, create_tables
from .routers import classifier, health

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500, detail="GROQ_API_KEY not found in .env file"
        )

    engine = create_db_engine()
    await create_tables(engine)

    app.state.session_factory = create_session_factory(engine)
    app.state.classifier_agent = classifier_agent

    yield

    # Cleanup resources
    await engine.dispose()


def get_application():
    return FastAPI(title="Dog Product Classifier API", lifespan=lifespan)


app = get_application()

app.include_router(classifier.router)
app.include_router(health.router)
app.include_router(products.router)
