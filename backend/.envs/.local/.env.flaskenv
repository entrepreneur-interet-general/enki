FLASK_ENV=development
FLASK_APP=src/entrypoints/flask_app
DEBUG=True
SECRET_KEY=changeme
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=redis://redis
#REPOSITORIES=PG # "if empty repos fallback to in memory"
SQLALCHEMY_SGE_ENGINE_OPTIONS=postgresql://hub:hub@hubdb:5432/hub

