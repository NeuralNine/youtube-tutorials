# NOTE: New Code

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from celery.result import AsyncResult

from main.tasks import movie_info


def index(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        async_res = movie_info.delay(prompt)

        return redirect(reverse("status") + f"?task_id={async_res.id}")

    return render(request, "main/index.html")


def status(request):
    task_id = request.GET.get("task_id")

    result = AsyncResult(task_id)
    context = {"task_id": task_id, "ready": result.ready(), "state": result.state}

    if result.ready():
        context["result"] = result.get()

    return render(request, "main/status.html", context)

