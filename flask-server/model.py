import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
import gensim
from nltk.tokenize import word_tokenize
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from collections import Counter
from nltk.corpus import stopwords
from flask import request, jsonify, Blueprint
from dotenv import load_dotenv
import os
from supabase_py import create_client

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client with environment variables
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_API_KEY')
supabase = create_client(supabase_url, supabase_key)

# Create Blueprint for model routes
model_bp = Blueprint('model', __name__)

# Define function to initialize the model
def initialize_model(journal_entry):
    # Load the English language model for spaCy
    nlp = spacy.load("en_core_web_sm")

    # Journal entry
    # journal_entry = ""

    # Get the English stopwords
    stop_words = set(stopwords.words('english'))

    # Add punctuation to the list of stop words
    stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', 'with', 'of', 'and', 'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'from', 'by', 'as', 'was', 'were', 'is', 'am', 'are', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'his', 'hers', 'ours', 'theirs', 'day', 'today'])

    # Apply VADER sentiment analysis
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(journal_entry)
    print("VADER Sentiment Score:", sentiment_score)

    # Process the journal entry with spaCy for entity extraction
    doc = nlp(journal_entry)

    # Tokenize the journal entry
    tokens = word_tokenize(journal_entry.lower())

    # Filter out the stop words
    filtered_tokens = [token for token in tokens if token not in stop_words]

    # Create a gensim dictionary from the filtered tokens
    dictionary = Dictionary([filtered_tokens])

    # Create a bag-of-words corpus
    corpus = [dictionary.doc2bow([token]) for token in filtered_tokens]

    # Initialize an LDA model
    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=10)

    # Count the frequency of each word
    word_freq = Counter(filtered_tokens)

    # Sort the dictionary by value in descending order and store the keys in an array
    most_repeated_words = [word for word, freq in word_freq.most_common(5) if word not in stop_words]

    # Extract entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    print("Entities:", entities)

    # Print the most repeated words
    print("topic keywords:", most_repeated_words)
    
    return sentiment_score, entities, most_repeated_words

# Define route for running the model
@model_bp.route('/api/run-model', methods=['POST'])
def run_model():
    data = request.json  # Assuming JSON data is sent from the frontend
    # Process the input data and run your model here
    print("data received is")
    print(data)
    entryText = data.get('entry_text')
    entryID = data.get('entry_id')
    print("fetched data")
    print(entryText)
    print("entry id", entryID)
    # Call initialize_model to get the values
    sentiment_score, entities, most_repeated_words = initialize_model(entryText)

 # Save the data to the analysis_data table
    response = supabase.table('analysis_data').insert([{
        'entry_id': entryID,  # Add the entry ID to the data
        'sentiment_score': sentiment_score,
        'topic_keywords': most_repeated_words,
        'entity_extraction': entities
    }])
    
    # Check if the insertion was successful
    if response.error is None:
        print("Data saved successfully to analysis_data table.")
    else:
        print("Failed to save data to analysis_data table:", response.error)


    # Return the results
    return jsonify({
        'sentiment_score': sentiment_score,
        'entities': entities,
        'topic_keywords': most_repeated_words
    }) 
