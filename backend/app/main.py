from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from fastapi_pagination import add_pagination
from starlette.staticfiles import StaticFiles

from app.api.db import async_session
from app.api.routers.user_router import router as user_router
from app.api.routers.auth_router import router as auth_router
from app.api.routers.game_router import router as game_router
from app.api.routers.team_router import router as team_router
from app.api.routers.match_router import router as match_router
from app.api.routers.image_router import router as image_router

app = FastAPI()
app.sa_sessionmaker = async_session
add_pagination(app)

app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(user_router)
app.include_router(auth_router)
app.include_router(game_router)
app.include_router(team_router)
app.include_router(match_router)
app.include_router(image_router)


@app.exception_handler(ValueError)
async def unicorn_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.get("/")
async def read_root():
    return {"message": "Server is healthy"}
