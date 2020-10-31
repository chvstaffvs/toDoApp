from uvicorn import run
from fastapi import FastAPI
import models
from routes import router

app = FastAPI(title="To Do API")

app.include_router(router)

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000, reload=True)