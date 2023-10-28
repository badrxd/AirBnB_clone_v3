#!/usr/bin/python3
""" Api v1 entrypoint for AirBnB v3 flask project"""
from flask import Flask, make_response
from models import storage, storage_t
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.url_map.strict_slashes = False
HBNB_API_HOST = getenv("HBNB_API_HOST")
HBNB_API_PORT = getenv("HBNB_API_PORT")
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_request(error):
    """remove the current SQLAlchemy Session after each request"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """return error 404
    Responses:
      404:
        description: set for not found paths
    """
    return make_response({'error': 'Not found'}, 404)


if __name__ == '__main__':
    """ start code just if tha name == main"""
    host = '0.0.0.0'
    port = 5000
    if storage_t == "db":
        host = HBNB_API_HOST
        port = HBNB_API_PORT
    app.run(host=host, port=port, threaded=True)
