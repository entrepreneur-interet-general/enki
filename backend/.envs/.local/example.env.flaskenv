FLASK_ENV=development
FLASK_APP=src/entrypoints/flask_app
DEBUG=True
SECRET_KEY=changeme
DATABASE_URI=postgresql://postgres:pg-password@postgres:5432/sapeurs-dev

#### TWILIO
TWILIO_ACCOUNT_SID=aski-it
TWILIO_AUTH_TOKEN=ask-it

#### Not used for now
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=redis://redis

