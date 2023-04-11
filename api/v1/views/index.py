#!/usr/bin/python3
""" Script that starts a Flask app """
from api.v1.views import app_views
from flask import jsonify
from models import storage
import json


@app_views.route("/status")
def status():
    """ Returns the app status """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def stats():
    """ Retrieves the number of objects per each type """
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    dic = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    json_dict = json.dumps(dic, indent=2)
    return json_dict
