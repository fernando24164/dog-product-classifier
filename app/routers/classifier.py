from fastapi import APIRouter, Depends
from pydantic_ai import Agent
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ..deps import get_classifier_agent, get_db_session_factory
from ..schemas.models import DogProduct, ProductCategory
from ..services.classifier_service import classify_product

router = APIRouter(prefix="/classify", tags=["classifier"])


@router.post("/", response_model=ProductCategory)
async def classify_product_endpoint(
    product: DogProduct,
    agent: Agent = Depends(get_classifier_agent),
    db_session_factory: async_sessionmaker[AsyncSession] = Depends(
        get_db_session_factory
    ),
):
    """
    Classify a dog product into categories based on its name and description.

    Returns:
        ProductCategory: The classification result with category, confidence score, and subcategories
    """
    return await classify_product(product, agent, db_session_factory)
