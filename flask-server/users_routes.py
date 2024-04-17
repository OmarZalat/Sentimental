from flask import Blueprint, jsonify, request
from supabase_py import create_client
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client with environment variables
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_API_KEY')
supabase = create_client(supabase_url, supabase_key)

user_bp = Blueprint('user', __name__)

# Example route to fetch user data from the 'users' table
@user_bp.route('/api/users', methods=['GET'])
def get_users():
    # Query data from the 'users' table
    result = supabase.table('users').select().execute()
    # Get the data from the result
    data = result['data']
    return jsonify(data)

# @user_bp.route('/auth/google/callback', methods=['POST'])
# def google_auth_callback():
#     token = request.json.get('token')
#     return {'message': 'User authenticated successfully'}, 200