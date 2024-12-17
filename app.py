from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.auth import router as router_auth

app = FastAPI(title="Auto Fill Docs Api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)

app.include_router(router_auth)

@app.get("/")
async def root():
    return {"message": 'Api "Auto Fill Docs" here'}
