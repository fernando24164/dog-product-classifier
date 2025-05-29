from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ..deps import get_db_session_factory
from ..models.database import Product
from ..schemas.models import ProductCategory

router = APIRouter(tags=["products"])


@router.get("/products", response_model=List[ProductCategory])
async def get_all_products(
    db_session_factory: async_sessionmaker[AsyncSession] = Depends(
        get_db_session_factory
    ),
):
    """
    Get all classified products from the database.

    Returns:
        List[ProductCategory]: A list of all classified products
    """
    async with db_session_factory() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()

        return [
            ProductCategory(
                category=product.category,
                confidence=product.confidence,
                subcategories=product.subcategories.split(",")
                if product.subcategories
                else [],
            )
            for product in products
        ]
