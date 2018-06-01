import os

from app import create_app

from celery import Celery


# Tasks list
CELERY_TASK_LIST = []

# Generate tasks list
task_dir = os.path.join(os.path.dirname(__file__), 'tasks')
for filename in os.listdir(task_dir):
    if filename.endswith('.py'):
        CELERY_TASK_LIST.append('app.tasks.' + filename[:-3])


def make_celery(app):
    """
    Creates Celery app with flask app context.

    :param app: Flask app
    :return: Celery app instance
    """

    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        include=CELERY_TASK_LIST
    )
    celery.conf.update(app.config)

    # Attach Flask app context
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


# Create celery object
app = create_app()
celery = make_celery(app)
