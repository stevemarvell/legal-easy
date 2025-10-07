from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(title="Random Number API")

# CORS: allow only known frontend origins (and localhost for local dev)
# Update these if your frontend domains change.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://frontend.railway.com:8888",
        "https://frontend-production-497b.up.railway.app:8888",
    ],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d{1,5})?$",
    allow_credentials=False,  # set to True only if you actually use cookies/auth across origins
    allow_methods=["GET"],  # narrow to used methods
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
