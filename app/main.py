from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.endpoints import users, auth, telegram_clients
from app.services.message_service import run_multiple_clients, clients


@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_multiple_clients()

    yield

    for client in clients:
        await client.disconnect()

    print("All clients stopped.")


# Create the FastAPI app using the lifespan handler
app = FastAPI(lifespan=lifespan)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(telegram_clients.router, prefix="/clients", tags=["clients"])


@app.get("/")
async def read_root(self):
    return {"message": "Welcome to FastAPI!"}
