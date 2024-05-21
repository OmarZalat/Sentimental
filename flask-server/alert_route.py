from flask import Blueprint, jsonify
import random
from quotes_routes import fetch_quotes  # Import the function to fetch quotes

alert_bp = Blueprint('alert', __name__)

@alert_bp.route('/api/alert')
def alert():
    quotes = fetch_quotes()  # Fetch the quotes
    if quotes:
        random_quote = random.choice(quotes)  # Randomly select a quote
        alert_message = random_quote['quote_text']  # Assuming each quote has a 'quote_text' field
    else:
        alert_message = "No quotes available."

    return jsonify({'alert_message': alert_message})
