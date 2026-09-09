from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.redis_client import redis_backend
from src.core.rabbit_client import rabbit_backend
from src.api.v1.jobs import router as jobs_router
from src.api.v1.users import router as users_router

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

app = FastAPI(
    title="Job Board API (Clean Architecture)",
    description="Проект сайта вакансий с FastAPI, PostgreSQL, Redis и RabbitMQ",
    version="1.0.0",
    lifespan=lifespan,
    debug=True
)

# Подключаем роутеры с префиксом версии API
app.include_router(jobs_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the Job Board API! Go to /docs for Swagger UI."}

