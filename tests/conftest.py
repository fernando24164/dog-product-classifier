import os

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch


@pytest.fixture
def client():
    """Return a TestClient for the FastAPI app."""
    os.environ["GROQ_API_KEY"] = "test-key"
    from app.main import app
    return TestClient(app)

@pytest.fixture
def mock_classifier_agent():
    """Mock the classifier agent to avoid actual API calls."""
    with patch("app.deps.get_classifier_agent") as mock_agent:
        agent_instance = AsyncMock()
        mock_agent.return_value = agent_instance
        
        mock_result = AsyncMock()
        mock_result.output = AsyncMock()
        mock_result.output.category = "Toys"
        mock_result.output.confidence = 0.95
        mock_result.output.subcategories = ["Chew Toys", "Interactive Toys"]
        
        agent_instance.run.return_value = mock_result
        
        yield agent_instance