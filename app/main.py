from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routes.v1 import user
from app.routes.v1 import account, auth
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

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(account.router, prefix="/accounts", tags=["accounts"])


@app.get("/")
async def read_root(self):
    return {"message": "Welcome to Telegram-Service!"}
