from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.core.logger import setup_logging
from backend.app.database import connect_to_mongo, close_mongo_connection
from backend.app.api.v1.health import router as health_router

setup_logging()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, version="0.1.0", docs_url="/docs")

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routes
    app.include_router(health_router, prefix="/api/v1")
    # Register planner router
    from backend.app.agents.planner.planner_router import router as planner_router

    app.include_router(planner_router, prefix="/api/v1/planner")
    # Register retrieval router
    from backend.app.agents.retrieval.retrieval_router import router as retrieval_router

    app.include_router(retrieval_router, prefix="/api/v1/retrieval")
    # Register orchestrator router
    from backend.app.orchestrator.orchestrator_router import router as orchestrator_router

    app.include_router(orchestrator_router, prefix="/api/v1/orchestrator")
    # Register satellite router
    from backend.app.agents.satellite.satellite_router import router as satellite_router

    app.include_router(satellite_router, prefix="/api/v1/satellite")
    # Register GIS router
    from backend.app.agents.gis.gis_router import router as gis_router

    app.include_router(gis_router, prefix="/api/v1/gis")
    # Register report router
    from backend.app.agents.report.report_router import router as report_router
    from backend.app.api.v1.report import router as report_api_router

    app.include_router(report_router, prefix="/api/v1/report")
    app.include_router(report_api_router, prefix="/api/v1/report")
    # Register files router
    from backend.app.api.v1.files import router as files_router
    app.include_router(files_router, prefix="/api/v1")
    # Register jobs router
    from backend.app.api.v1.jobs import router as jobs_router
    app.include_router(jobs_router, prefix="/api/v1/jobs")
    # Register auth router
    from backend.app.auth.auth_router import router as auth_router
    from backend.app.auth.middleware import FirebaseAuthMiddleware

    app.add_middleware(FirebaseAuthMiddleware)
    app.include_router(auth_router, prefix="/api/v1/auth")
    # Register ML router
    from backend.app.agents.ml.ml_router import router as ml_router

    app.include_router(ml_router, prefix="/api/v1/ml")

    # Monitoring middleware and routes
    from backend.app.monitoring.middleware import MonitoringMiddleware
    from backend.app.monitoring.monitoring_router import router as monitoring_router

    app.add_middleware(MonitoringMiddleware)
    app.include_router(monitoring_router, prefix="/api/v1/monitoring")

    @app.on_event("startup")
    async def startup_event() -> None:
        await connect_to_mongo()

    @app.on_event("shutdown")
    async def shutdown_event() -> None:
        await close_mongo_connection()

    return app


app = create_app()
