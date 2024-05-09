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

# Create Blueprint for journal routes
journal_bp = Blueprint('journal', __name__)

# Route to Add a New Journal Entry
# Route to Add a New Journal Entry
@journal_bp.route('/api/journal', methods=['POST'])
def add_journal_entry():
    print('Received POST request to /api/journal')
    entry_data = request.json

    # Log the received data
    print('Received data:', entry_data)

    # user_id = request.headers.get('user_id')

    # entry_data['user_id'] = user_id

    result = supabase.table('journal_entries').insert(entry_data).execute()

    # Log the result
    print('Insertion result:', result)
    if not result['data']:
        return jsonify({'error': 'Failed to add journal entry.'}), 500
    else:
        return jsonify({'message': 'Journal entry added successfully.'}), 200


# Route to Fetch Journal Entries
@journal_bp.route('/api/journal', methods=['GET'])
def get_journal_entries():
    result = supabase.table('journal_entries').select().execute()
    data = result['data']
    return jsonify(data)

#route to fetch a single journal entry according to the entry id
@journal_bp.route('/api/journal/<string:entry_id>', methods=['GET'])
def get_single_journal_entry(entry_id):
    result = supabase.table('journal_entries').select().eq('entry_id', entry_id).execute()
    data = result['data']
    return jsonify(data)


# Route to Delete a Journal Entry
@journal_bp.route('/api/journal/<int:entry_id>', methods=['DELETE'])
def delete_journal_entry(entry_id):
    result = supabase.table('journal_entries').delete().where('id', '=', entry_id).execute()

    if result['error']:
        return jsonify({'error': 'Failed to delete journal entry.'}), 500
    else:
        return jsonify({'message': 'Journal entry deleted successfully.'}), 200
