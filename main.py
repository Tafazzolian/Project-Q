from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Initiationg Project Q"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host="0.0.0.0", port=8090, reload=True)