from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import redis
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend to make requests
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to Redis (using Redis hostname since we'll use Docker Compose)
redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

# Rate limiting constants
RATE_LIMIT = 5  # Max 5 requests
TIME_WINDOW = 60  # Per 60 seconds

def is_rate_limited(user_id):
    current_time = int(time.time())
    redis_key = f"rate_limit:{user_id}"
    
    request_times = redis_client.lrange(redis_key, 0, -1)
    request_times = [int(t) for t in request_times]
    
    # Remove timestamps older than the TIME_WINDOW
    request_times = [t for t in request_times if current_time - t < TIME_WINDOW]
    redis_client.delete(redis_key)
    for t in request_times:
        redis_client.rpush(redis_key, t)
    
    if len(request_times) >= RATE_LIMIT:
        return True  # Rate limited

    # Add the current request timestamp
    redis_client.rpush(redis_key, current_time)
    redis_client.expire(redis_key, TIME_WINDOW)  # Set expiration time
    return False

@app.get("/api/resource")
async def get_resource(request: Request):
    user_id = request.client.host  # Use IP address as a simple identifier

    if is_rate_limited(user_id):
        return JSONResponse(content={"error": "Rate limit exceeded"}, status_code=429)

    return {"message": "Resource accessed successfully"}

