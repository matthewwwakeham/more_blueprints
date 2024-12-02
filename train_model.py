# imports
import joblib
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report
import pandas as pd

# Set up logging to log both to console and a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/model_training.log"),  # Log to file
        logging.StreamHandler()                         # Log to console
    ]
)

def train_and_save_model():
    # Load dataset
    faq_data = pd.read_csv('data/faq_dataset.csv')

    # Extract features and labels
    questions = faq_data['Question']
    intents = faq_data['Intent']  # Ensure the 'Intent' column exists in your dataset

    # Split the data into training and test sets for evaluation
    X_train, X_test, y_train, y_test = train_test_split(questions, intents, test_size=0.2, random_state=42)

    # Vectorize the questions
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))  # Added stop_words and ngram_range for better vectorization
    X_train_vect = vectorizer.fit_transform(X_train)
    X_test_vect = vectorizer.transform(X_test)

    # Train a simple classifier with class weights to handle imbalance
    model = LogisticRegression(max_iter=200, class_weight='balanced')  # Use class weight to handle imbalance
    model.fit(X_train_vect, y_train)

    # Define the stratified k-fold cross-validation with 3 splits
    skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

    # Evaluate the model using stratified k-fold cross-validation
    cv_scores = cross_val_score(model, X_train_vect, y_train, cv=skf)
    logging.info(f"Cross-validation scores: {cv_scores}")
    logging.info(f"Mean cross-validation score: {cv_scores.mean()}")

    # Predict and evaluate the model
    y_pred = model.predict(X_test_vect)
    report = classification_report(y_test, y_pred, zero_division=1)  # Suppress zero division warnings
    logging.info("Model Evaluation Report:\n" + report)  # Log classification report

    # Save the model and vectorizer
    joblib.dump(model, 'app/models/intent_model.pkl')
    joblib.dump(vectorizer, 'app/models/intent_vectorizer.pkl')

    logging.info("Model and vectorizer saved successfully!")

# Run the training and saving process
train_and_save_model()