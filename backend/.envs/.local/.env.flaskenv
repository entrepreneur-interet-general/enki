FLASK_ENV=development
FLASK_APP=src/entrypoints/flask_app
DEBUG=True
SECRET_KEY=changeme
SQLALCHEMY_SGE_ENGINE_OPTIONS=postgresql://hub:hub@hubdb:5432/hub
DATABASE_URI=postgresql://postgres:pg-password@localhost:5432/sapeurs-dev
#REPOSITORIES=PG # "if empty repos fallback to in memory"



#### Not used for now
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=redis://redis
