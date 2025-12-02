"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.pdf_router import router as pdf_router
from app.api.mcq_router import router as mcq_router


def create_app() -> FastAPI:
    """Initialize FastAPI app with routers and middleware."""
    app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, debug=settings.DEBUG)

    # Support multiple frontend URLs (for production deployment)
    frontend_urls = [settings.FRONTEND_URL]
    if settings.FRONTEND_URLS:
        frontend_urls.extend([url.strip() for url in settings.FRONTEND_URLS.split(",") if url.strip()])
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=frontend_urls,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(pdf_router)
    app.include_router(mcq_router)

    @app.get("/")
    async def root():
        return {
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "running",
        }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

