from fastapi import APIRouter

# Create an APIRouter for product-related routes
router = APIRouter(
    prefix="/api/products",
    tags=["Products"]
)

