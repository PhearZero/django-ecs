from time import sleep
from celery import shared_task


@shared_task()
def go_to_sleep_task(length: int):
    """Sends an email when the feedback form has been submitted."""
    print("Go to Sleep")
    sleep(length)  # Simulate expensive operation(s) that freeze Django
    print("Awake")
