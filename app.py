from fastapi import FastAPI

app = FastAPI(title="Auto Fill Docs Api")


@app.get("/")
async def root():
    return {"message": 'Api "Auto Fill Docs" here'}
