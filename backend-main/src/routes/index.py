from flask import Blueprint

from src.routes.chatbot_route import chatbot_routes
from src.routes.quiz_info_route import quiz_info_routes
from src.routes.planets_list_route import planets_list_routes

prediction_bp = Blueprint('prediction_bp', __name__)

def init_app(app):
    # Register sub-blueprints
    prediction_bp.register_blueprint(chatbot_routes)
    prediction_bp.register_blueprint(quiz_info_routes)
    prediction_bp.register_blueprint(planets_list_routes)

    # Register the main blueprint
    app.register_blueprint(prediction_bp)

    app.logger.info("Registered main prediction_bp blueprint")
    app.logger.info("All blueprints have been registered")