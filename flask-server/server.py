from flask import Flask, Response, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import datetime
from flask_cors import CORS
from dotenv import load_dotenv
import os
import secrets
from users_routes import user_bp
from analysis_routes import analysis_bp
from prompt_routes import prompt_bp
from quotes_routes import quotes_bp
from journal_routes import journal_bp
from model import model_bp
from alert_route import alert_bp

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register blueprints for routes
app.register_blueprint(user_bp)
app.register_blueprint(analysis_bp)
app.register_blueprint(prompt_bp)
app.register_blueprint(quotes_bp)
app.register_blueprint(journal_bp)
app.register_blueprint(model_bp)
app.register_blueprint(alert_bp)

if __name__ == "__main__":
    app.run(debug=True)
