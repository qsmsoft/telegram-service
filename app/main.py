from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cli.cli import logger

from app.db.config import init_db, engine
from app.routes import user
from app.services.message_service import run_multiple_clients, clients


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # await init_db()
        await run_multiple_clients()
        yield

    finally:
        for client in clients:
            await client.disconnect()

        # await engine.dispose()

    logger.info("All clients stopped.")


# Create the FastAPI app using the lifespan handler
app = FastAPI(lifespan=lifespan)

app.include_router(user.router, prefix="/users", tags=["users"])


# app.include_router(account.router, prefix="/accounts", tags=["accounts"])


@app.get("/")
async def read_root(self):
    return {"message": "Welcome to Telegram-Service!"}
