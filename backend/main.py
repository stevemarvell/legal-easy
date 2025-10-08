from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(title="Random Number API")

# CORS: allow frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080", 
        "http://127.0.0.1:8080",
        "https://legal-easy-frontend-production.up.railway.app", 
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"]
)

@app.get("/random")
def get_random():
    """Return a random integer between 0 and 100 inclusive."""
    return {"value": random.randint(0, 100)}

@app.get("/")
def root():
    return {"message": "Random Number API. Use /random"}
