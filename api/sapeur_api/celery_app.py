from .app import init_celery

app = init_celery()
app.conf.imports = app.conf.imports + ("sapeur_api.tasks.example",)
