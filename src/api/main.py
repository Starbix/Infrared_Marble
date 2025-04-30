from fastapi import FastAPI

from api.routers.explore_router import router as explore_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"version": "1.0.0", "status": "ok"}


app.include_router(explore_router)
