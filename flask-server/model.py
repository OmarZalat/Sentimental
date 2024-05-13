import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
import gensim
from nltk.tokenize import word_tokenize
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from collections import Counter
from nltk.corpus import stopwords


# Load the English language model for spaCy
nlp = spacy.load("en_core_web_sm")

# Journal entry
journal_entry = "Today was a memorable day filled with exciting experiences. I started the morning with a refreshing jog in Central Park, enjoying the vibrant colors of the sunrise. Afterward, I visited the Metropolitan Museum of Art to admire the stunning exhibits showcasing ancient artifacts and modern masterpieces. In the afternoon, I attended a business meeting at the headquarters of Google, where I discussed innovative ideas with talented professionals. Later, I met up with my friend Sarah at a cozy café in Greenwich Village, where we shared stories and laughter over cups of delicious coffee. As the day came to a close, I watched a captivating performance at the Lincoln Center, mesmerized by the talented musicians and dancers on stage. Reflecting on the day's adventures, I feel grateful for the enriching experiences and meaningful connections that have made today truly special."

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
print("topic keywords:",most_repeated_words)

