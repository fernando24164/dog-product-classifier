from fastapi import APIRouter, Depends
from pydantic_ai import Agent

from ..deps import get_classifier_agent
from ..models import DogProduct, ProductCategory
from ..services.classifier_service import classify_product

router = APIRouter(prefix="/classify", tags=["classifier"])

@router.post("/", response_model=ProductCategory)
async def classify_product_endpoint(
    product: DogProduct,
    agent: Agent = Depends(get_classifier_agent),
):
    """
    Classify a dog product into categories based on its name and description.
    
    Returns:
        ProductCategory: The classification result with category, confidence score, and subcategories
    """
    return await classify_product(product, agent)
