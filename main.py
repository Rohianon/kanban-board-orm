from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import data

app = FastAPI(
    title="KB Board ORM",
    version="0.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router)