from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from users_routes import user_bp
from analysis_routes import analysis_bp
from prompt_routes import prompt_bp
from quotes_routes import quotes_bp

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register blueprints for routes
app.register_blueprint(user_bp)
app.register_blueprint(analysis_bp)
app.register_blueprint(prompt_bp)
app.register_blueprint(quotes_bp)

if __name__ == "__main__":
    app.run(debug=True)
