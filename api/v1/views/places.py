#!/usr/bin/python3
""" Flask application for Place class/entity """
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from flask import jsonify, abort, request


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def retrieves_all_places(city_id):
    """Returns the list of all Place objects"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = city.places
    places_list = []
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """ Returns an object by id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes an object by id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """ Creates an object """
    place_data = request.get_json()
    city = storage.get(City, city_id)
    user = place_data.get('user_id')
    if not city:
        abort(404)
    elif not place_data:
        abort(400, "Not a JSON")
    elif "user_id" not in place_data:
        abort(400, "Missing user_id")
    elif not user:
        abort(404)
    elif "name" not in place_data:
        abort(400, "Missing name")
    place_data["city_id"] = city_id
    new_place = Place(**place_data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """ Updates an object """
    place_data = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    elif not place_data:
        abort(400, "Not a JSON")

    for key, value in place_data.items():
        if key not in ["id", "state_id", "city_id",
                       "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
