from flask import Blueprint, request, jsonify
from src.controllers.index import chatbot_controllers

chatbot_routes = Blueprint('chatbot_routes', __name__)

@chatbot_routes.route('/chatbot_route',methods=['POST'])
def chatbot():
    try:
        data = request.get_json()
        resp,code = chatbot_controllers.generate_chat(data)
        return jsonify(resp),code
    except Exception as e:
        return jsonify({"message"f"An error occurred {e}"}),500