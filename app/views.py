from django.shortcuts import render
from django.views.decorators.http import require_GET

from app.tasks import go_to_sleep_task


@require_GET
def index(request):
    go_to_sleep_task.delay(30)
    return render(
        request,
        "base.html",
        {
            "title": "Django on ECS",
        },
    )
