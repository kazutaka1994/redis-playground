from fastapi import FastAPI

from .api.routes import router

app = FastAPI(
    title="Redis Caching API",
    description="RedisキャッシングとPostgreSQLを使用したユーザーAPI",
    version="1.0.0",
)

app.include_router(router, prefix="/api/v1", tags=["users"])


@app.get("/")
async def root():
    return {"message": "Redis Caching API", "docs": "/docs", "status": "ok"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
