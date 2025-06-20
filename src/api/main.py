from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.comparison_router import router as comparison_router
from api.routers.explore_router import router as explore_router
from api.routers.statistics_router import router as statistics_router
from lib.config import LJ_METADATA_DOWNLOAD_DIR
from lib.lj import lj_download_metadata

app = FastAPI()

# CORS Stuff
origins = ["http://localhost", "http://localhost:3000", "http://localhost:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pre-emptively download LuoJia metadata
if not LJ_METADATA_DOWNLOAD_DIR.exists():
    lj_download_metadata()


@app.get("/")
def read_root():
    return {"version": "1.0.0", "status": "ok"}


@app.get("/health")
def read_health():
    return {"status": "ok"}


app.include_router(explore_router)
app.include_router(comparison_router)
app.include_router(statistics_router)
