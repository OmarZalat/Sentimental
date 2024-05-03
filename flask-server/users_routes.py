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

# Route to fetch user data from the 'users' table
@user_bp.route('/api/users', methods=['GET'])
def get_users():
    # Query data from the 'users' table
    result = supabase.table('users').select().execute()
    # Get the data from the result
    data = result['data']
    return jsonify(data) 

# Route to receive user data from the frontend and save it to the 'users' table
@user_bp.route('/api/user', methods=['POST'])
def save_user():
    # Get the user data from the request body
    user_data = request.get_json()

    # Structure the data for insertion into the 'users' table
    data_to_insert = {
        'username': user_data.get('given_name'),
        'email': user_data.get('email'),
    }

    # Insert the user data into the 'users' table
    result = supabase.table('users').insert(data_to_insert).execute()

    # Return a success message
    return jsonify({'message': 'User data saved successfully'})