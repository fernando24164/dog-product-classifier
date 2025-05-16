from typing import List

from fastapi import HTTPException
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.exceptions import UnexpectedModelBehavior

from ..models import DogProduct, ProductCategory


class ClassificationOutput(BaseModel):
    category: str = Field(
        ..., description="The most appropriate category for the product"
    )
    confidence: float = Field(
        ..., description="Confidence score between 0 and 1", ge=0, le=1
    )
    subcategories: List[str] = Field(
        ..., description="Relevant subcategories for the product"
    )


PRODUCT_CATEGORIES = [
    "Food",
    "Toys",
    "Grooming",
    "Accessories",
    "Health",
    "Training",
    "Bedding",
]


def create_classification_prompt(product: DogProduct, categories: List[str]) -> str:
    """Generate a prompt for the AI agent to classify a dog product."""
    return f"""  
    Please classify the following dog product:  
      
    Name: {product.name}  
    Description: {product.description}  
      
    Available categories: {", ".join(categories)}  
      
    Respond with the most appropriate category, a confidence score (0-1), and relevant subcategories.  
    """


async def classify_product(
    product: DogProduct, agent: Agent, categories: List[str] = PRODUCT_CATEGORIES
) -> ProductCategory:
    """
    Classify a dog product using the AI agent.

    Args:
        product: The dog product to classify
        agent: The AI agent to use for classification
        categories: Available product categories

    Returns:
        ProductCategory object with classification results
    """
    try:
        prompt = create_classification_prompt(product, categories)
        result = await agent.run(prompt, output_type=ClassificationOutput)
    except UnexpectedModelBehavior as e:
        raise HTTPException(status_code=500, detail=f"Unexpected model behavior: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {e}")

    return ProductCategory(
        category=result.output.category,
        confidence=result.output.confidence,
        subcategories=result.output.subcategories,
    )
