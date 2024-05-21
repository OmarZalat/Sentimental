from flask import Blueprint, jsonify, request
from supabase_py import create_client
import os
from dotenv import load_dotenv
from model import initialize_model
import requests
import random

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client with environment variables
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_API_KEY')
supabase = create_client(supabase_url, supabase_key)

# Create Blueprint for journal routes
journal_bp = Blueprint('journal', __name__)

@journal_bp.route('/api/journal', methods=['POST'])
def add_journal_entry():
    print('Received POST request to /api/journal')
    entry_data = request.json
    print('Received data:', entry_data)
    entry_text = entry_data.get('entry_text')

    sentiment_score, entities, most_repeated_words = initialize_model(entry_text)

    # Ensure sentiment_score is a dictionary if it's stored as text in the database
    if isinstance(sentiment_score, str):
        sentiment_score = json.loads(sentiment_score)

    result = supabase.table('journal_entries').insert(entry_data).execute()
    print('Insertion result:', result)

    if not result['data']:
        return jsonify({'error': 'Failed to add journal entry.'}), 500

    entry_id = result['data'][0]['entry_id']

    analysis_result = supabase.table('analysis_data').insert([{
        'entry_id': entry_id,
        'sentiment_score': sentiment_score,  # Store as dictionary
        'topic_keywords': most_repeated_words,
        'entity_extraction': entities
    }]).execute()

    print('Analysis result:', analysis_result)

    if not analysis_result['data']:
        return jsonify({'error': 'Failed to add analysis data.'}), 500

    compound_score = sentiment_score.get('compound')
    print(compound_score)
    alert_message = None

    if compound_score < 0:
        try:
            response = requests.get("http://localhost:5000/api/alert")
            if response.status_code == 200:
                alert_message = response.json().get('alert_message')
            else:
                print('Failed to fetch alert message')
        except Exception as e:
            print('Error calling alert route:', e)

    # Fetch prompts from the existing prompts route
    try:
        prompts_response = requests.get("http://localhost:5000/api/prompts")
        if prompts_response.status_code == 200:
            prompts = prompts_response.json()

            # Filter prompts by type
            topic_prompts = [prompt['prompt_text'] for prompt in prompts if prompt['type'] == 'topic']
            emotion_prompts = [prompt['prompt_text'] for prompt in prompts if prompt['type'] == 'emotions']
            intent_prompts = [prompt['prompt_text'] for prompt in prompts if prompt['type'] == 'intent']

            # Select one random prompt from each type
            topic_prompt = random.choice(topic_prompts) if topic_prompts else None
            emotion_prompt = random.choice(emotion_prompts) if emotion_prompts else None
            intent_prompt = random.choice(intent_prompts) if intent_prompts else None

            print('Random Topic Prompt:', topic_prompt)
            print('Random Emotion Prompt:', emotion_prompt)
            print('Random Intent Prompt:', intent_prompt)
        else:
            print('Failed to fetch prompts')
    except Exception as e:
        print('Error fetching prompts:', e)

    return jsonify({
        'message': 'Journal entry and analysis data added successfully.',
        'alert_message': alert_message,
        'prompts': {
            'topic': topic_prompt,
            'emotion': emotion_prompt,
            'intent': intent_prompt
        }
    }), 200


@journal_bp.route('/api/journal', methods=['GET'])
def get_journal_entries():
    result = supabase.table('journal_entries').select().execute()
    data = result['data']
    return jsonify(data)

@journal_bp.route('/api/journal/<string:entry_id>', methods=['GET'])
def get_single_journal_entry(entry_id):
    result = supabase.table('journal_entries').select().eq('entry_id', entry_id).execute()
    data = result['data']
    return jsonify(data)