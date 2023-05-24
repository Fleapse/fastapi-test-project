import asyncio
from fastapi import FastAPI
import typer
from apps import routers
from .db import init_models

app = FastAPI()

for router in routers:
    app.include_router(router)
