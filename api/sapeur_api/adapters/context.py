class SQLContext(object):

    def __init__(self):
        self.task_repository = None
        self.user_repository = None
        self.db = None

    def init_app(self, app, db):
        from .repositories import UserRepository, TaskRepository
        app.context = self
        self.task_repository = TaskRepository(db)
        self.user_repository = UserRepository(db)
        self.db = db

    def setup(self):
        self.db.create_all()
