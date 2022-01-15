
from fastapi import FastAPI
from starlette.requests import Request
from datetime import datetime
from routes.v1 import app_v1


app = FastAPI(
    title="OCR API Documentation",
    description="API for detect text in images",
    version="1.0.0",
)


app.include_router(
    app_v1,
    prefix="/v1"
)




@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()

    response = await call_next(request)

    # modify response
    execution_time = (datetime.utcnow() - start_time).microseconds
    response.headers["x-execution-time"] = str(execution_time)
    return response