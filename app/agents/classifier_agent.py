import os
from dataclasses import dataclass

from dotenv import load_dotenv
from fastapi import HTTPException
from pydantic_ai import Agent, RunContext
from pydantic_ai.providers.groq import GroqProvider
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ..models.database import Product
from ..schemas.models import ProductCategory

load_dotenv()


api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    raise HTTPException(status_code=500, detail="GROQ_API_KEY not found in .env file")


@dataclass
class DbDeps:
    db_session_factory: async_sessionmaker[AsyncSession]
    product_category: ProductCategory


provider = GroqProvider(api_key=api_key)

classifier_agent = Agent(
    "groq:llama-3.1-8b-instant",
    provider=provider,
    deps_type=DbDeps,
    system_prompt="""
        You are a dog product classification expert. Your task is to classify dog products into the most appropriate category.  
        Analyze the product name and description carefully to determine the best category.  
        Provide a confidence score between 0 and 1, where 1 is the highest confidence.  
        Also suggest relevant subcategories for the product.
        Ensure that your response is always formatted as a ClassificationOutput.
        If you detect that the product is not intended for dogs, lower the confidence score accordingly.

        When asked to save classification results, do not try to pass any parameters to the save_dog_product_classification function.
        The function automatically uses the context that contains all necessary information.
        Simply call the function without any parameters.
        """,
)


@classifier_agent.tool
async def save_dog_product_classification(ctx: RunContext[DbDeps]) -> None:
    """Save the dog product classification to the database.

    This function doesn't take any direct parameters as they are provided through the context.
    The product classification details are already available in ctx.deps.product_category.

    Args:
        ctx: Run context containing database dependencies with product_category information

    Returns:
        None
    """
    try:
        async with ctx.deps.db_session_factory() as session:
            subcategories_str = ",".join(ctx.deps.product_category.subcategories)
            product = Product(
                category=ctx.deps.product_category.category,
                confidence=ctx.deps.product_category.confidence,
                subcategories=subcategories_str,
            )
            session.add(product)
            await session.commit()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error while saving classification: {str(e)}",
        )
