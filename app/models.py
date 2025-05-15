from typing import List
from pydantic import BaseModel, Field


class DogProduct(BaseModel):
    name: str = Field(..., description="Name of the dog product")
    description: str = Field(..., description="Description of the dog product")


class ProductCategory(BaseModel):
    category: str = Field(..., description="Category of the dog product")
    confidence: float = Field(
        ..., description="Confidence score of the classification", ge=0, le=1
    )
    subcategories: List[str] = Field(
        default_factory=list, description="Subcategories of the dog product"
    )
