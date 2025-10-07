from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(title="Random Number API")

# CORS: allow frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",  # Frontend dev server
        "http://127.0.0.1:8080",
        "https://frontend.railway.com:8888",
        "https://frontend-production-497b.up.railway.app:8888",
    ],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d{1,5})?$",
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)

@app.get("/random")
def get_random():
    """Return a random integer between 0 and 100 inclusive."""
    return {"value": random.randint(0, 100)}

# Optional root route for quick check
@app.get("/")
def root():
    return {"message": "Random Number API. Use /random"}
