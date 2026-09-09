pip3 install \
  "fastapi[all]" \
  sqlalchemy \
  alembic \
  psycopg2-binary \
  pydantic-settings \
  celery \
  redis \
  python-dotenv



# Вакансии
POST   /api/v1/jobs              - Создать вакансию
GET    /api/v1/jobs              - Список с фильтрацией и кешем
GET    /api/v1/jobs/{id}         - Деталь вакансии
PUT    /api/v1/jobs/{id}         - Обновить
DELETE /api/v1/jobs/{id}         - Удалить

# Подписки (Feature 1)
POST   /api/v1/subscriptions     - Создать подписку
GET    /api/v1/subscriptions     - Мои подписки
DELETE /api/v1/subscriptions/{id} - Отписаться

# Статистика (Feature 2)
GET    /api/v1/jobs/stats/trending - Популярные вакансии
GET    /api/v1/search/popular    - Популярные поиски


pip install alembic
alembic init -t async migrations
