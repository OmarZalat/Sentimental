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
@journal_bp.route('/api/journal', methods=['POST'])
def add_journal_entry():
    entry_data = request.json

    result = supabase.table('journal_entries').insert(entry_data).execute()

    if result['error']:
        return jsonify({'error': 'Failed to add journal entry.'}), 500
    else:
        return jsonify({'message': 'Journal entry added successfully.'}), 201

# Route to Fetch Journal Entries
@journal_bp.route('/api/journal', methods=['GET'])
def get_journal_entries():
    result = supabase.table('journal_entries').select().execute()
    data = result['data']
    return jsonify(data)

# Route to Update a Journal Entry
@journal_bp.route('/api/journal/<int:entry_id>', methods=['PUT'])
def update_journal_entry(entry_id):
    updated_entry_data = request.json

    result = supabase.table('journal_entries').update(updated_entry_data).where('id', '=', entry_id).execute()

    if result['error']:
        return jsonify({'error': 'Failed to update journal entry.'}), 500
    else:
        return jsonify({'message': 'Journal entry updated successfully.'}), 200

# Route to Delete a Journal Entry
@journal_bp.route('/api/journal/<int:entry_id>', methods=['DELETE'])
def delete_journal_entry(entry_id):
    result = supabase.table('journal_entries').delete().where('id', '=', entry_id).execute()

    if result['error']:
        return jsonify({'error': 'Failed to delete journal entry.'}), 500
    else:
        return jsonify({'message': 'Journal entry deleted successfully.'}), 200
