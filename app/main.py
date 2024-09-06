from fastapi import FastAPI

from app.api.v1.endpoints import users, userbotinfos
from app.db.session import engine
from app.models.user import Base

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the user API router
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(userbotinfos.router, prefix="/accounts", tags=["accounts"])


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}
