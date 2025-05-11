from fastapi import FastAPI
import uvicorn
from routes.user_routes import router as user_router


def create_app():
    """Create a FastAPI app."""
    return FastAPI()


app = create_app()

@app.get("/")
def read_root():
    return {"message": "Hello World"}



app.include_router(user_router)




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    