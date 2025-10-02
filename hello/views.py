import random
import threading
import time

from django.http import HttpResponse
from django.shortcuts import render

from .models import Greeting

# Create your views here.


def index(request):
    return render(request, "index.html")

def ao_custom(request):
    # counts
    print("count#user.clicks=1")
    print("count#user.clicks.tagged=1 tag#user_id=2 tag#user_geo=earth")
    print("source=us-west count#user.clicks.sourced=1")
    # measures
    print("measure#database.query=200ms")
    print("measure#database.query.tagged=200ms tag#db_name=foo tag#db_type=postgres")
    print("source=us-east measure#database.query.sourced=200ms")
    # samples
    print("sample#database.size=40.9MB")
    print("sample#database.size.tagged=40.9MB tag#db_name=foo tag#db_type=postgres")
    print("source=another-source sample#database.size.sourced=40.9MB")
    return render(request, "index.html")


def db(request):
    # If you encounter errors visiting the `/db/` page on the example app, check that:
    #
    # When running the app on Heroku:
    #   1. You have added the Postgres database to your app.
    #   2. You have uncommented the `psycopg` dependency in `requirements.txt`, and the `release`
    #      process entry in `Procfile`, git committed your changes and re-deployed the app.
    #
    # When running the app locally:
    #   1. You have run `./manage.py migrate` to create the `hello_greeting` database table.

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

def sleep(request):
    # sleep for query parameter `ms` milliseconds, or random duration up to 3s if not specified.
    try:
        sleep_s = int(request.GET["ms"]) / 1000
    except (KeyError, ValueError):
        sleep_s = random.uniform(0, 3.0)
    print(f"sleeping {sleep_s}s")
    time.sleep(sleep_s)
    return HttpResponse(f"slept {sleep_s} seconds", content_type="text/plain")

def status(request):
    # return query parameter `code` as status code, or 400 if not specified.
    # throw unhandled exception on invalid value.
    status_code = int(request.GET.get("code", 400))
    if status_code < 100 or status_code > 599:
        raise ValueError("status code invalid range")
    return HttpResponse(f"status {status_code}", content_type="text/plain", status=status_code)

def resource(request):
    # simulate memory allocation and cpu load.
    # get size in KB and thread count from query parameters `kb` and `threads`.
    try:
        size_kb = int(request.GET["kb"]) * 1024
    except (KeyError, ValueError):
        size_kb = 10 * 1024

    try:
        threads_count = int(request.GET["threads"])
    except (KeyError, ValueError):
        threads_count = 16

    def memory_and_cpu_load(tid, memory_size_kb):
        data = bytearray(memory_size_kb * 1024)
        end_time = time.time() + 5 # run for 5 seconds
        iterations = 0
        while time.time() < end_time:
            _ = sum(i ** 2 for i in range(1000))
            iterations += 1
        info[tid] = iterations
        del data

    info = {}
    threads = []
    for i in range(threads_count):
        thread = threading.Thread(target=memory_and_cpu_load, args=(i, size_kb,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    return HttpResponse(str(info), content_type="text/plain")