import os

from celery import Celery

from app import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery('app')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

redbeat_redis_url = settings.REDIS_URL

count = 0
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, debug_scheduled_task.s('hello-10'), name='add every 10')

    # Calls test('hello') every 30 seconds.
    # It uses the same signature of previous task, an explicit name is
    # defined to avoid this task replacing the previous one defined.
    sender.add_periodic_task(30.0, debug_scheduled_task.s('hello-30'), name='add every 30')

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task()
def debug_scheduled_task(arg):
    global count
    count += 1
    print(f"{arg}-{count}")
