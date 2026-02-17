from app.routes import user_routes, auth_routers
from app.config.database_config import Base, engine
from app.config.env_config import env_config
from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Security",
    description="FastAPI Security",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


app.include_router(user_routes.router)
app.include_router(auth_routers.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=env_config.app_host,
        port=env_config.app_port,
        reload=True,
        log_level="info",
    )
