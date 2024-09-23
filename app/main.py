import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.endpoints import users, accounts, auth, sessions as telegram_sessions
from app.db.session import engine
from app.models.user import Base
from app.services.message_service import client

# Create the database tables
Base.metadata.create_all(bind=engine)

sessions = []


async def run_existing_sessions():
    print('Running existing sessions...')
    await asyncio.gather(*[asyncio.sleep(1) for _ in sessions])


@asynccontextmanager
async def lifespan(app: FastAPI):
    client_task = asyncio.create_task(client.start())
    session_task = asyncio.create_task(run_existing_sessions())

    try:
        yield  # This starts the FastAPI app while tasks run in the background
    finally:
        # Shutdown: Cancel the tasks when FastAPI shuts down
        await client.stop()
        client_task.cancel()
        session_task.cancel()

        # Await tasks to ensure proper cancellation
        await asyncio.gather(client_task, session_task, return_exceptions=True)


# Create the FastAPI app using the lifespan handler
app = FastAPI(lifespan=lifespan)

# Include the user API router
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(telegram_sessions.router, prefix="/sessions", tags=["sessions"])


@app.get("/")
async def read_root(self):
    return {"message": "Welcome to FastAPI!"}
