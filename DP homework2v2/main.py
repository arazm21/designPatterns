from typing import Dict

import uvicorn
from fastapi import FastAPI

from controllers.product_controller import router as product_router
from controllers.receipt_controller import router as receipt_router
from controllers.sales_controller import router as sales_router
from controllers.unit_controller import router as unit_router
from database.init_db import initialize_database

app = FastAPI()

# Register routers
app.include_router(unit_router)
app.include_router(product_router)
app.include_router(receipt_router)
app.include_router(sales_router)

@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Hello, World!"}

# Initialize database
@app.on_event("startup")
def startup() -> None:
    initialize_database()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
# @app.get("/products/{product_id}")
# def get_product(product_id: str):
#     return {"product_id": product_id, "name": "Sample Product", "price": 100}


# from fastapi import FastAPI
#
# app = FastAPI()
#
#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
