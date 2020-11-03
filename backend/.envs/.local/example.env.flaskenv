FLASK_ENV=development
FLASK_APP=src/entrypoints/flask_app
DEBUG=True
SECRET_KEY=changeme
DATABASE_SGE_URI=postgresql://hub:hub@hubdb:5432/hub
DATABASE_URI=postgresql://postgres:pg-password@postgres:5432/sapeurs-dev

#### Not used for now
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=redis://redis

