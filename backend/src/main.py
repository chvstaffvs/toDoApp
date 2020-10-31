from uvicorn import run
from fastapi import FastAPI


app = FastAPI(title="To Do API")

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000)