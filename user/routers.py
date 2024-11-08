from fasttower.routers import APIRouter

from user.views import router as user_router

router = APIRouter(prefix="/user", tags=["user"])

router.include_router(user_router)
