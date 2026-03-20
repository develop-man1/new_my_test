from fastapi import APIRouter, Depends

from ..dependencies.auth import require_permission
from ..models.user import User

router = APIRouter(prefix="/business", tags=["Business"])


@router.get("/products")
async def get_products(_: User = Depends(require_permission("products", "read"))):
    return {
        "items": [
            {"id": 1, "name": "Laptop", "price": 999.99},
            {"id": 2, "name": "Phone", "price": 499.99},
            {"id": 3, "name": "Tablet", "price": 299.99},
        ]
    }


@router.post("/products")
async def create_product(_: User = Depends(require_permission("products", "create"))):
    return {"message": "Product created (mock)"}


@router.get("/orders")
async def get_orders(_: User = Depends(require_permission("orders", "read"))):
    return {
        "items": [
            {"id": 1, "product": "Laptop", "status": "delivered"},
            {"id": 2, "product": "Phone", "status": "pending"},
        ]
    }


@router.delete("/orders/{order_id}")
async def delete_order(order_id: int, _: User = Depends(require_permission("orders", "delete"))):
    return {"message": f"Order {order_id} deleted (mock)"}