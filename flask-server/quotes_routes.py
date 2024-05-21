from flask import Blueprint, jsonify
from supabase_py import create_client
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client with environment variables
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_API_KEY')
supabase = create_client(supabase_url, supabase_key)

# Create Blueprint for quotes routes
quotes_bp = Blueprint('quotes', __name__)

# Function to fetch quotes
def fetch_quotes():
    result = supabase.table('quotes').select().execute()
    return result['data']

# Route to Fetch Quotes
@quotes_bp.route('/api/quotes', methods=['GET'])
def get_quotes():
    data = fetch_quotes()
    return jsonify(data)
