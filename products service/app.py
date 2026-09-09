from fastapi import FastAPI

app=FastAPI(title="Product Service API")

@app.get("/health-check")
def health_check():
    return {"status":True,"message":"Welcome to product service module!"}