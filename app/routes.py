import logging
from flask import Blueprint, request, jsonify, render_template, redirect, session, url_for, flash
from .models import User
from . import db
from utils import get_random_color
from .chatbot_logic import load_chatbot_resources, get_response
from datetime import datetime

# Define blueprint
chat_bp = Blueprint('chat', __name__, template_folder='templates')

# Load chatbot resources
questions, answers, intents, intent_model, intent_vectorizer, faq_vectorizer = load_chatbot_resources()

# Module-specific logger
logger = logging.getLogger(__name__)

# Home route
@chat_bp.route('/')
def home():
    if "username" in session:
        return redirect(url_for('chat.dashboard'))
    return render_template('index.html')

# Login
@chat_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_or_email = request.form.get('username') or request.form.get('email')
        password = request.form.get("password")

        if not username_or_email:
            flash('Please enter a valid username or email.', 'error')
            return redirect(url_for('chat.login'))
        
        try:
            user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()
            if user and user.check_password(password):
                session['username'] = user.username
                session['email'] = user.email
                session['user_color'] = user.user_color
                logger.info(f"User {user.username} logged in.")
                return redirect(url_for('chat.dashboard'))
            else:
                flash('Invalid username or password.', 'error')
        except Exception as e:
            logger.error(f"Login error: {e}")
            flash('An error occurred while logging in. Please try again.', 'error')
        return redirect(url_for('chat.login'))
    
    return render_template('login.html')

# Register
@chat_bp.route('/register', methods=['POST'])
def register():
    try:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('User already exists.', 'error')
            return redirect(url_for('chat.signup'))

        user_color = get_random_color()
        new_user = User(username=username, email=email, user_color=user_color)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        session['email'] = email
        session['user_color'] = user_color
        logger.info(f"New user registered: {username}")
        return redirect(url_for('chat.dashboard'))
    except Exception as e:
        logger.error(f"Registration error: {e}")
        flash('An error occurred while creating your account. Please try again.', 'error')
        return redirect(url_for('chat.signup'))
    
# Password Reset
@chat_bp.route("/reset")
def reset():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template("chat.reset.html")

# Signup page
@chat_bp.route('/signup')
def signup():
    if "username" in session:
        return redirect(url_for('chat.dashboard'))
    return render_template('signup.html')

# Logout
@chat_bp.route('/logout')
def logout():
    session.clear()
    logger.info("User logged out.")
    return redirect(url_for('chat.home'))

# Dashboard
@chat_bp.route('/dashboard')
def dashboard():
    if "username" in session:
        return render_template(
            'dashboard.html',
            username=session['username'],
            email=session.get('email'),
            user_color=session.get('user_color')
        )
    return redirect(url_for('chat.home'))

# Chatbot API
@chat_bp.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')

    if not user_input:
        logger.warning("Empty message received.")
        return jsonify({'error': 'No message provided.'}), 400

    if len(user_input) > 140:
        logger.warning(f"Message exceeds character limit: {len(user_input)}")
        return jsonify({'error': 'Message exceeds 140 characters.'}), 400

    timestamp = datetime.now().strftime("%H:%M")
    try:
        response = get_response(user_input, questions, answers, intents, intent_model, intent_vectorizer, faq_vectorizer)
        logger.info(f"User: {user_input} | Bot: {response}")
        return jsonify({
            'user_message': {'message': user_input, 'timestamp': timestamp},
            'bot_response': {'message': response, 'timestamp': timestamp}
        })
    except Exception as e:
        logger.error(f"Chatbot error: {e}")
        return jsonify({'error': 'An error occurred while processing your message.'}), 500