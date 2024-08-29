import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .database import lifespan
from .routers import main, auth


def create_app() -> FastAPI:
    debug = not os.getenv("APP_ENV") == "PROD"
    app = FastAPI(
        lifespan=lifespan,
        debug=debug,
        openapi_url="/openapi.json" if debug else None,
        docs_url="/docs" if debug else None,
        redoc_url="/redoc" if debug else None,
        title="Schedule",
        version="0.1.0",
    )

    current_dir = os.path.dirname(os.path.realpath(__file__))
    static_dir = os.path.join(current_dir, ".", "static")
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    app.add_middleware(
        SessionMiddleware, secret_key="0c94f0f7-a1b3-41c9-9d6a-56a7fd156fcc"
    )
    # if debug:
    #     app.add_middleware(
    #         DebugToolbarMiddleware,
    #         panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"],
    #     )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    app.include_router(main.router)
    app.include_router(auth.router)

    return app


app = create_app()
