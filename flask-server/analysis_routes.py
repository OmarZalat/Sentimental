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

# Create Blueprint for analysis routes
analysis_bp = Blueprint('analysis', __name__)

# Route to Fetch Analysis Data
@analysis_bp.route('/api/analysis', methods=['GET'])
def get_analysis_data():
    result = supabase.table('analysis_data').select().execute()
    data = result['data']
    return jsonify(data)

# Add more analysis-related routes as needed...
