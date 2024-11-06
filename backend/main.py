import os
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import redis
import time
import jwt
import datetime
from pydantic import BaseModel



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend to make requests
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to Redis (using Redis hostname since we'll use Docker Compose)
redis_client = redis.StrictRedis(host=os.getenv('redis_host'), port=6379, db=0, decode_responses=True)

SECRET_KEY = os.getenv("Token")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username : str
    
dummy_user = {
        "username" : "Username"

    }

# Rate limiting constants
RATE_LIMIT = 5  # Max 5 requests
TIME_WINDOW = 60  # Per 60 seconds
RATE_LIMIT_HR = 15
TIME_WINDOW_HR = 3600 

def is_rate_limited(user_id):
    current_time = int(time.time())
    redis_key = f"rate_limit:{user_id}"
    
    request_times = redis_client.lrange(redis_key, 0, -1)
    request_times = [int(t) for t in request_times]
    
    # Remove timestamps older than the TIME_WINDOW
    request_times_min = [t for t in request_times if current_time - t < TIME_WINDOW ]
    request_times_hr = [t for t in request_times if current_time - t < TIME_WINDOW_HR]
    redis_client.delete(redis_key)
    for t in request_times:
        redis_client.rpush(redis_key, t)
    
    if len(request_times_min) >= RATE_LIMIT:
        return True  # Rate limited
    
    if len(request_times_hr) >= RATE_LIMIT_HR:
        return True

    # Add the current request timestamp
    redis_client.rpush(redis_key, current_time)
    redis_client.expire(redis_key, TIME_WINDOW)  # Set expiration time
    return False


def create_access_token(data:dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)})
    return jwt.encode(to_encode,SECRET_KEY,algorithms=ALGORITHM)


@app.post("/token")
def login_for_access_token(form_data: User):
    if form_data.username != dummy_user["username"]:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    token = create_access_token(data={"sub":form_data.username})
    return {"access_token" : token,"token_type": "bearer"}


@app.get("/api/resource/v1")
def get_resource(request: Request):
    user_id = request.client.host
    if is_rate_limited(user_id):
        return JSONResponse(content={"error": "Rate Limit exceeded"}, status_code=429)
    return {"message" : "Resource accessed successfully"}

@app.get("/api/resource/v2")
def get_resource_jwt(request: Request, token: str = Depends(oauth2_scheme)):
    user_id = request.client.host  # Use IP address as a simple identifier
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        if username is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    
    if is_rate_limited(user_id):
        return JSONResponse(content={"error": "Rate limit exceeded"}, status_code=429)

    return {"message": "Resource accessed successfully"}

