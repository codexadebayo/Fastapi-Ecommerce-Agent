from fastapi import FastAPI
import uvicorn


def create_app():
    """Create a FastAPI app."""
    return FastAPI()


app = create_app()

@app.get("/")
def read_root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    