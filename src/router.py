from fastapi import APIRouter, FastAPI

from src.apps.account.router import account_router
from src.apps.user.routers.user_routers import user_router

router = APIRouter(prefix='/api/v1')
router.include_router(account_router)
router.include_router(user_router)


def apply_router(app: FastAPI) -> FastAPI:
    app.include_router(router)
    return app
