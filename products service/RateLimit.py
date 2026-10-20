import redis.asyncio as redis 
from fastapi import Request,HTTPException
import time

# Initialize an async Redis connection pool
redis_client = redis.from_url("redis://localhost:6379/0", decode_responses=True)

class RateLimiter:
    def __init__(self, times: int, seconds: int):
        self.times = times
        self.seconds = seconds

    async def __call__(self, request: Request):
        # Identify the client by their IP address
        client_ip = request.client.host
        route_path = request.url.path
        
        # Create a unique key based on the current time window block
        window_bucket = int(time.time() // self.seconds)
        redis_key = f"rate_limit:{client_ip}:{route_path}:{window_bucket}"

        # Increment the counter atomically
        current_requests = await redis_client.incr(redis_key)

        # If it's the first request in this window, set the expiration
        if current_requests == 1:
            await redis_client.expire(redis_key, self.seconds)

        # Check if the client exceeded the allowed limit
        if current_requests > self.times:
            raise HTTPException(
                status_code=429, 
                detail="Too many requests. Please try again later."
            )