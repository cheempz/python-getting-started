from django.shortcuts import render

from .models import Greeting

# Create your views here.


def index(request):
    return render(request, "index.html")

def aocustom(request):
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
