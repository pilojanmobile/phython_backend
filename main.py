from fastapi import FastAPI

app=FastAPI()


@app.get("/")
async def Home():
    return {'message' : "Working fine"}