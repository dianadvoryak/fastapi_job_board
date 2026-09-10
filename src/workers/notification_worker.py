import asyncio
import json
import sys
import os

# Фиксим пути импорта, чтобы запускать скрипт напрямую
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import aio_pika
from src.core.config import settings


async def process_notification(message: aio_pika.IncomingMessage):
    """Callback-функция, которая срабатывает при получении сообщения из очереди."""
    async with message.process():  # Автоматически подтверждает (ACK) сообщение, если код не упал
        # Декодируем входящий JSON
        payload = json.loads(message.body.decode("utf-8"))

        print(f"\n[ВОРКЕР] Получено событие по вакансии #{payload['job_id']}")
        print(f"[ВОРКЕР] Анализируем навыки: {payload['tags']}")

        # Имитируем тяжелую фоновую работу (поиск совпадений в БД, отправка Email через SMTP)
        await asyncio.sleep(3)

        print(
            f"[ВОРКЕР] Уведомления соискателям о вакансии '{payload['title']}' в '{payload['company']}' успешно отправлены!\n")


async def main():
    # Подключаемся к RabbitMQ
    connection = await aio_pika.connect_robust(
        f"amqp://{settings.RABBIT_USER}:{settings.RABBIT_PASSWORD}@{settings.RABBIT_HOST}:{settings.RABBIT_PORT}/"
    )
    channel = await connection.channel()

    # Ограничиваем воркера: обрабатывать только 1 задачу за раз (чтобы не перегружать память)
    await channel.set_qos(prefetch_count=1)

    # Декларируем очередь
    queue = await channel.declare_queue("job_notifications", durable=True)

    print(" [*] Воркер рассылки уведомлений запущен. Ожидание сообщений. Нажмите CTRL+C для выхода.")

    # Начинаем слушать очередь
    await queue.consume(process_notification)

    # Держим процесс запущенным
    try:
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main())
