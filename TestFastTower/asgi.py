"""
ASGI config for TestFastTower project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os

from fasttower.utils import setup

from TestFastTower.database import init_db

os.environ.setdefault("FASTTOWER_SETTINGS_MODULE", "TestFastTower.settings")
setup()

from fasttower import FastTower

from TestFastTower.routers import router


app = FastTower(title="FastTower API Documentation")


@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(router)
