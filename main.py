from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.redis_client import redis_backend
from src.core.rabbit_client import rabbit_backend

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Действия при старте приложения
    redis_backend.init()
    await rabbit_backend.connect()
    print("::: Инициализированы подключения к Redis и RabbitMQ :::")
    yield
    # Действия при остановке приложения
    await redis_backend.close()
    await rabbit_backend.close()
    print("::: Подключения к Redis и RabbitMQ закрыты :::")

app = FastAPI(lifespan=lifespan)
