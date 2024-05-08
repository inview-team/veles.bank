from fastapi import APIRouter, FastAPI

from src.apps.wallet.router import wallet_router
from src.apps.auth.router import auth_router
from src.apps.user.routers.user_routers import user_router
from src.apps.company.router import company_router

router = APIRouter(prefix='/api/v1')

router.include_router(wallet_router)
router.include_router(user_router)
router.include_router(auth_router)
router.include_router(company_router)


def apply_router(app: FastAPI) -> FastAPI:
    app.include_router(router)
    return app
