FLASK_ENV=development
FLASK_APP=sapeur_api.app:create_app
SECRET_KEY=changeme
DATABASE_URI=sqlite:////tmp/sapeur_api.db
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=amqp://guest:guest@localhost/
