from fasttower.routers import APIRouter

from user.routers import router as user_router

router = APIRouter(prefix="/api/v1", tags=["api"])
router.include_router(user_router)
