from fastapi import FastAPI
from app.routers import health, lookup, validate, history
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()


# Include Routers
app.include_router(health.router)
app.include_router(lookup.router)
app.include_router(validate.router)
app.include_router(history.router)


@app.get("/")
async def root():
    import time
    import os


    return {
        "version": "0.1.0",
        "date": int(time.time()),
        "kubernetes": os.getenv("KUBERNETES_SERVICE_HOST") is not None
    }

instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, endpoint="/metrics")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000, log_level="info")
