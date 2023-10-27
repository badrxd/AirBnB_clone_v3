""" Api v1 entrypoint index route"""
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def status():
    """return json"""
    return {"status": "OK"}


@app_views.route("/stats")
def count():
    """return stats counts"""
    return storage.count()
