from fastapi import FastAPI

from app.routers import products

app = FastAPI(title="Cinch Product Rental API")
app.include_router(products.router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to Cinch Product Rental API"}
