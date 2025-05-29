import pytest
from unittest.mock import MagicMock


@pytest.fixture(autouse=True)
def setup_app_state(client, mock_classifier_agent):
    """Setup app state with mocked dependencies."""
    client.app.state.classifier_agent = mock_classifier_agent
    client.app.state.session_factory = MagicMock()
    yield
    client.app.state.classifier_agent = None
    client.app.state.session_factory = None


class TestClassifier:
    def test_classify_product_happy_path(self, client):
        """Test successful product classification."""
        test_product = {
            "name": "Durable Chew Bone",
            "description": "Long-lasting chew toy for aggressive chewers. Made from durable rubber.",
        }

        response = client.post("/classify", json=test_product)

        assert response.status_code == 200
        result = response.json()
        assert result["category"] == "Toys"
        assert result["confidence"] == 0.95
        assert "Chew Toys" in result["subcategories"]
        assert "Interactive Toys" in result["subcategories"]
        assert len(result["subcategories"]) == 2
