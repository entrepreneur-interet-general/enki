class SQLContext(object):
    def __init__(self, db):
        from .repositories import UserRepository, TaskRepository

        self.db = db

        self.task_repository = TaskRepository(db)
        self.user_repository = UserRepository(db)

    def setup(self):
        self.db.create_all()
