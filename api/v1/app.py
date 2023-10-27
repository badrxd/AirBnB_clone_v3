from flask import Flask
app = Flask(__name__)
from models import storage, storage_t
from api.v1.views import app_views
from os import getenv

HBNB_API_HOST = getenv("HBNB_API_HOST")
HBNB_API_PORT = getenv("HBNB_API_PORT")
# print(HBNB_API_HOST,HBNB_API_PORT)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_request(error):
    """remove the current SQLAlchemy Session after each request"""
    storage.close()


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    if storage_t == "db":
        host = HBNB_API_HOST
        port = HBNB_API_PORT
    app.run(host=host, port=port,threaded=True)