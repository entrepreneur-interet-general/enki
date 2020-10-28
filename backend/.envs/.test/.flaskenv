FLASK_ENV=development
FLASK_APP="myapp.app:create_app"
SECRET_KEY=testing
DATABASE_URI=sqlite:///:memory:
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=amqp://guest:guest@localhost/
