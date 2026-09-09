import aio_pika
from src.core.config import settings


class RabbitMQBackend:
    def __init__(self):
        self.connection: aio_pika.RobustConnection | None = None
        self.channel: aio_pika.RobustChannel | None = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(
            f"amqp://{settings.RABBIT_USER}:{settings.RABBIT_PASSWORD}@{settings.RABBIT_HOST}:{settings.RABBIT_PORT}/"
        )
        self.channel = await self.connection.channel()

        # Декларируем очереди заранее, чтобы они создались при старте приложения
        await self.channel.declare_queue("job_notifications", durable=True)
        await self.channel.declare_queue("resume_generation", durable=True)

    async def close(self):
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()


rabbit_backend = RabbitMQBackend()


# Dependency для отправки сообщений в роутерах/сервисах
async def get_rabbit_channel() -> aio_pika.RobustChannel:
    return rabbit_backend.channel
