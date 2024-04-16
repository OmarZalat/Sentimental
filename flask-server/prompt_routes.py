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

# Create Blueprint for prompt routes
prompt_bp = Blueprint('prompt', __name__)

# Route to Fetch Prompts
@prompt_bp.route('/api/prompts', methods=['GET'])
def get_prompts():
    result = supabase.table('prompts_templates').select().execute()
    data = result['data']
    return jsonify(data)

# Add more prompt-related routes as needed...
