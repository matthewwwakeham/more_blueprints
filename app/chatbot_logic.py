import logging
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

# Set up a custom logger for chatbot logic
chatbot_logger = logging.getLogger("chatbot_logger")
chatbot_logger.setLevel(logging.INFO)

# File handler for chatbot logs
chatbot_handler = logging.FileHandler('logs/intent_logs.log')
chatbot_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
chatbot_logger.addHandler(chatbot_handler)

# Load dataset and models
def load_chatbot_resources():
    # Read the q&a + intents CSV
    faq_data = pd.read_csv('data/faq_dataset.csv')
    
    # Extract questions, answers, and intents from the CSV
    questions = faq_data['Question'].tolist()
    answers = faq_data['Answer'].tolist()
    intents = faq_data['Intent'].tolist()
    
    # Load intent prediction model and vectorizer
    intent_model = joblib.load('app/models/intent_model.pkl')
    intent_vectorizer = joblib.load('app/models/intent_vectorizer.pkl')

    # Initialize and fit a single vectorizer for FAQ questions
    faq_vectorizer = TfidfVectorizer()
    faq_vectorizer.fit(questions)
    
    return questions, answers, intents, intent_model, intent_vectorizer, faq_vectorizer

def get_response(user_query, questions, answers, intents, intent_model, intent_vectorizer, faq_vectorizer):
    # Vectorize the user query for intent prediction
    query_vec_intent = intent_vectorizer.transform([user_query])
    predicted_intent = intent_model.predict(query_vec_intent)[0]
    intent_confidence = max(intent_model.predict_proba(query_vec_intent)[0])  # Confidence score
    
    # Log user query and predicted intent
    chatbot_logger.info(f"User Query: {user_query}")
    chatbot_logger.info(f"Predicted Intent: {predicted_intent} (Confidence: {intent_confidence:.2f})")
    
    # Check if predicted intent is valid
    if predicted_intent in intents:
        chatbot_logger.info(f"Valid Intent: {predicted_intent}")
    else:
        chatbot_logger.warning(f"Unknown Intent: {predicted_intent}")
        return "I'm sorry, I didn't understand that. Could you rephrase?"
    
    # Vectorize the user query for FAQ matching
    query_vec_faq = faq_vectorizer.transform([user_query])
    tfidf_matrix = faq_vectorizer.transform(questions)
    similarity = cosine_similarity(query_vec_faq, tfidf_matrix)
    best_match = similarity.argmax()
    similarity_score = similarity[0, best_match]
    
    # Log FAQ matching details
    chatbot_logger.info(f"FAQ Match: {questions[best_match]} (Similarity: {similarity_score:.2f})")
    
    # Return an appropriate response based on similarity threshold
    if similarity_score > 0.2:  # Adjust threshold as needed
        return answers[best_match]
    else:
        chatbot_logger.warning(f"No suitable match found for: {user_query}")
        return "I'm sorry, I don't have an answer for that. Please contact support."