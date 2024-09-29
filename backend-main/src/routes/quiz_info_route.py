from flask import Blueprint, request, jsonify
from src.controllers.index import quiz_info_controller

quiz_info_routes = Blueprint('quiz_info_routes', __name__)

@quiz_info_routes.route('/quiz_route',methods=['POST'])
def quiz():
    try:
        data = request.get_json()
        resp,code = quiz_info_controller.generate_quiz(data)
        print(resp)
        return jsonify(resp),code
    except Exception as e:
        return jsonify({"message"f"An error occurred {e}"}),500

@quiz_info_routes.route('/info_route',methods=['POST'])
def info():
    try:
        data = request.get_json()
        resp,code = quiz_info_controller.generate_info(data)
        print(resp)
        return jsonify(resp),code
    except Exception as e:
        return jsonify({"message"f"An error occurred {e}"}),500