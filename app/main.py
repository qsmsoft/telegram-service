import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.endpoints import users, auth, telegram_clients
from app.services.message_service import start_clients


# Create the database tables
# Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    client_task = asyncio.create_task(start_clients())
    try:
        yield
    finally:
        client_task.cancel()
        await client_task


# Create the FastAPI app using the lifespan handler
app = FastAPI(lifespan=lifespan)

# Include the user API router
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(telegram_clients.router, prefix="/clients", tags=["clients"])


@app.get("/")
async def read_root(self):
    return {"message": "Welcome to FastAPI!"}
