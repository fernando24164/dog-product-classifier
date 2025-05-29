from unittest.mock import AsyncMock, MagicMock


class TestProducts:
    def test_get_all_products(self, client, monkeypatch):
        """Test retrieving all classified products."""
        mock_products = [
            MagicMock(
                category="Toys",
                confidence=0.95,
                subcategories="Chew Toys,Interactive Toys",
            ),
            MagicMock(
                category="Food", confidence=0.88, subcategories="Dry Food,Treats"
            ),
        ]

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_products

        mock_session = AsyncMock()
        mock_session.__aenter__.return_value.execute.return_value = mock_result

        mock_session_factory = MagicMock()
        mock_session_factory.return_value = mock_session

        client.app.state.session_factory = mock_session_factory

        monkeypatch.setattr(
            "app.deps.get_db_session_factory", lambda: mock_session_factory
        )

        response = client.get("/products")

        assert response.status_code == 200
        products = response.json()
        assert len(products) == 2

        assert products[0]["category"] == "Toys"
        assert products[0]["confidence"] == 0.95
        assert products[0]["subcategories"] == ["Chew Toys", "Interactive Toys"]

        assert products[1]["category"] == "Food"
        assert products[1]["confidence"] == 0.88
        assert products[1]["subcategories"] == ["Dry Food", "Treats"]

        client.app.state.session_factory = None
