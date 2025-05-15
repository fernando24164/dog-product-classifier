from fastapi import Request
from pydantic_ai import Agent
from pydantic_ai.providers.groq import GroqProvider


def get_groq_provider(request: Request) -> GroqProvider:
    """
    Get the Groq provider from app.state.

    Args:
        request: The FastAPI request object

    Returns:
        The Groq provider instance
    """
    return request.app.state.groq_provider


def get_classifier_agent(request: Request) -> Agent:
    """
    Get the classifier agent from app.state.

    Args:
        request: The FastAPI request object

    Returns:
        The classifier agent instance
    """
    return request.app.state.classifier_agent
