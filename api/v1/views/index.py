#!/usr/bin/python3
""" Api v1 entrypoint index route"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    """return json"""
    return {"status": "OK"}


@app_views.route("/stats")
def count():
    """return stats counts"""
    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}

    counts = {}
    for key, value in classes.items():
        counts[key] = storage.count(value)
    return counts
