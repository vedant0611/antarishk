from flask import Blueprint, request, jsonify
from src.controllers.index import planets_list_controllers

planets_list_routes = Blueprint('planets_list_routes', __name__)

@planets_list_routes.route('/planets_list_route',methods=['GET'])
def planets_list():
    try:
        resp,code = planets_list_controllers.planets_list()
        print("resp",resp)
        return jsonify(resp),code
    except Exception as e:
        return jsonify({"message"f"An error occurred {e}"}),500