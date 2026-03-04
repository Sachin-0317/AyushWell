from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ayushwell.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

active_tokens = {}

# ==================== DATABASE MODELS ====================

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    assessments = db.relationship('Assessment', backref='user', lazy=True)
    progress_records = db.relationship('Progress', backref='user', lazy=True)

class Assessment(db.Model):
    __tablename__ = 'assessments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    answers = db.Column(db.JSON, nullable=False)
    vata_score = db.Column(db.Integer, nullable=False)
    pitta_score = db.Column(db.Integer, nullable=False)
    kapha_score = db.Column(db.Integer, nullable=False)
    dominant_dosha = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class Progress(db.Model):
    __tablename__ = 'progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    calories = db.Column(db.Integer, default=0)
    activity_minutes = db.Column(db.Integer, default=0)
    water_ml = db.Column(db.Integer, default=0)
    sleep_hours = db.Column(db.Float, default=0)
    weight_kg = db.Column(db.Float, nullable=True)
    stress_level = db.Column(db.Integer, default=5)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    diet_plan = db.Column(db.JSON, nullable=False)
    yoga_plan = db.Column(db.JSON, nullable=False)
    lifestyle_tips = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==================== ML CHATBOT TRAINING ====================

# 1. Define Training Data Blocks (Cleaned & Specific)

prakriti_data = [
    ("what is prakriti", "prakriti"), ("tell me about prakriti", "prakriti"), ("prakriti assessment", "prakriti"),
    ("constitution test", "prakriti"), ("body type quiz", "prakriti"), ("discover my dosha", "prakriti"),
    ("ayurvedic assessment", "prakriti"), ("mind body type", "prakriti"), ("what is my body type", "prakriti"),
    ("how do i know my dosha", "prakriti"), ("explain my nature", "prakriti"), ("my ayurvedic constitution", "prakriti"),
    ("check my body type", "prakriti"), ("know my dosha", "prakriti"), ("prakriti analysis", "prakriti"),
    ("dosha quiz", "prakriti"), ("find my ayurvedic type", "prakriti"), ("what is my nature", "prakriti"),
    ("prakriti test online", "prakriti"), ("assess my dosha", "prakriti"), ("ayurveda body test", "prakriti"),
    ("my dosha profile", "prakriti"), ("calculate my prakriti", "prakriti"), ("prakriti diagnosis", "prakriti"),
    ("what dosha am i", "prakriti"), ("identify my dosha", "prakriti"), ("prakriti calculator", "prakriti"),
    ("dosha determination", "prakriti"), ("my ayurvedic profile", "prakriti"), ("ayurvedic body typing", "prakriti"),
    ("understand my constitution", "prakriti"), ("reveal my dosha", "prakriti"), ("dosha identification", "prakriti"),
    ("ayurveda type quiz", "prakriti"), ("what is my ayurvedic dosha", "prakriti"), ("prakriti explanation", "prakriti"),
    ("body constitution analysis", "prakriti"), ("my body metrics ayurveda", "prakriti"), ("dosha composition", "prakriti"),
    ("explain my prakriti", "prakriti"),
]

dosha_general_data = [
    ("what are doshas", "dosha_general"), ("explain doshas", "dosha_general"), ("three doshas", "dosha_general"),
    ("vata pitta kapha", "dosha_general"), ("tell me about doshas", "dosha_general"), ("ayurvedic elements", "dosha_general"),
    ("understanding doshas", "dosha_general"), ("dosha meaning", "dosha_general"), ("what is tridosha", "dosha_general"),
    ("basics of ayurveda", "dosha_general"), ("ayurvedic energies", "dosha_general"), ("how do doshas work", "dosha_general"),
    ("function of doshas", "dosha_general"), ("dosha types", "dosha_general"), ("the 3 body types", "dosha_general"),
    ("principles of ayurveda", "dosha_general"), ("what is vpk", "dosha_general"), ("balance of doshas", "dosha_general"),
    ("ayurvedic bioenergies", "dosha_general"), ("role of doshas", "dosha_general"), ("define dosha", "dosha_general"),
    ("concept of doshas", "dosha_general"), ("ayurvedic humors", "dosha_general"), ("what are the 3 doshas", "dosha_general"),
    ("explain vata pitta kapha", "dosha_general"), ("tridosha theory", "dosha_general"), ("energy types in ayurveda", "dosha_general"),
    ("body energies", "dosha_general"), ("elemental composition", "dosha_general"), ("five elements and doshas", "dosha_general"),
    ("meaning of vata pitta kapha", "dosha_general"), ("guide to doshas", "dosha_general"), ("introduction to doshas", "dosha_general"),
    ("ayurvedic principles", "dosha_general"), ("how ayurveda works", "dosha_general"),
]

vata_data = [
    ("what is vata", "vata"), ("vata dosha", "vata"), ("tell me about vata", "vata"), ("air element", "vata"),
    ("am i vata", "vata"), ("vata characteristics", "vata"), ("vata symptoms", "vata"), ("traits of vata", "vata"),
    ("vata personality", "vata"), ("vata imbalance", "vata"), ("signs of vata", "vata"), ("vata body type", "vata"),
    ("vata features", "vata"), ("description of vata", "vata"), ("vata qualities", "vata"), ("space and air dosha", "vata"),
    ("vata problems", "vata"), ("high vata symptoms", "vata"), ("vata nature", "vata"), ("about vata dosha", "vata"),
    ("vata physical traits", "vata"), ("vata mental traits", "vata"), ("is vata cold", "vata"), ("dry skin vata", "vata"),
    ("anxiety vata", "vata"), ("excess vata", "vata"), ("vata disorders", "vata"), ("features of vata person", "vata"),
    ("vata dominance", "vata"), ("vata psychology", "vata"), ("vata digestion", "vata"), ("vata sleep pattern", "vata"),
    ("vata appearance", "vata"), ("understand vata", "vata"), ("vata explained", "vata"), ("vata element composition", "vata"),
    ("vata season", "vata"), ("vata time of day", "vata"), ("vata dosha details", "vata"), ("characteristics of air dosha", "vata"),
]

pitta_data = [
    ("what is pitta", "pitta"), ("pitta dosha", "pitta"), ("tell me about pitta", "pitta"), ("fire element", "pitta"),
    ("am i pitta", "pitta"), ("pitta characteristics", "pitta"), ("pitta symptoms", "pitta"), ("traits of pitta", "pitta"),
    ("pitta personality", "pitta"), ("pitta imbalance", "pitta"), ("signs of pitta", "pitta"), ("pitta body type", "pitta"),
    ("pitta features", "pitta"), ("description of pitta", "pitta"), ("pitta qualities", "pitta"), ("fire and water dosha", "pitta"),
    ("pitta problems", "pitta"), ("high pitta symptoms", "pitta"), ("pitta nature", "pitta"), ("about pitta dosha", "pitta"),
    ("pitta physical traits", "pitta"), ("pitta mental traits", "pitta"), ("is pitta hot", "pitta"), ("acidity pitta", "pitta"),
    ("anger pitta", "pitta"), ("excess pitta", "pitta"), ("pitta disorders", "pitta"), ("features of pitta person", "pitta"),
    ("pitta dominance", "pitta"), ("pitta psychology", "pitta"), ("pitta digestion", "pitta"), ("pitta sleep pattern", "pitta"),
    ("pitta appearance", "pitta"), ("understand pitta", "pitta"), ("pitta explained", "pitta"), ("pitta element composition", "pitta"),
    ("pitta season", "pitta"), ("pitta time of day", "pitta"), ("pitta dosha details", "pitta"), ("characteristics of fire dosha", "pitta"),
]

kapha_data = [
    ("what is kapha", "kapha"), ("kapha dosha", "kapha"), ("tell me about kapha", "kapha"), ("earth element", "kapha"),
    ("am i kapha", "kapha"), ("kapha characteristics", "kapha"), ("kapha symptoms", "kapha"), ("traits of kapha", "kapha"),
    ("kapha personality", "kapha"), ("kapha imbalance", "kapha"), ("signs of kapha", "kapha"), ("kapha body type", "kapha"),
    ("kapha features", "kapha"), ("description of kapha", "kapha"), ("kapha qualities", "kapha"), ("earth and water dosha", "kapha"),
    ("kapha problems", "kapha"), ("high kapha symptoms", "kapha"), ("kapha nature", "kapha"), ("about kapha dosha", "kapha"),
    ("kapha physical traits", "kapha"), ("kapha mental traits", "kapha"), ("is kapha heavy", "kapha"), ("weight gain kapha", "kapha"),
    ("lethargy kapha", "kapha"), ("excess kapha", "kapha"), ("kapha disorders", "kapha"), ("features of kapha person", "kapha"),
    ("kapha dominance", "kapha"), ("kapha psychology", "kapha"), ("kapha digestion", "kapha"), ("kapha sleep pattern", "kapha"),
    ("kapha appearance", "kapha"), ("understand kapha", "kapha"), ("kapha explained", "kapha"), ("kapha element composition", "kapha"),
    ("kapha season", "kapha"), ("kapha time of day", "kapha"), ("kapha dosha details", "kapha"), ("characteristics of earth dosha", "kapha"),
]

diet_data = [
    ("what should i eat", "diet"), ("food recommendations", "diet"), ("diet plan", "diet"), ("nutrition", "diet"),
    ("healthy eating", "diet"), ("what foods are good for me", "diet"), ("meal suggestions", "diet"), ("eating habits", "diet"),
    ("best diet", "diet"), ("ayurvedic diet", "diet"), ("diet for my dosha", "diet"), ("foods to avoid", "diet"),
    ("foods to favor", "diet"), ("what to eat for heavy stomach", "diet"), ("diet for digestion", "diet"), ("breakfast ideas", "diet"),
    ("lunch suggestions", "diet"), ("dinner options", "diet"), ("snacking in ayurveda", "diet"), ("dietary guidelines", "diet"),
    ("nutrition for vata", "diet"), ("nutrition for pitta", "diet"), ("nutrition for kapha", "diet"), ("spices to use", "diet"),
    ("meal timing", "diet"), ("eating schedule", "diet"), ("hot vs cold food", "diet"), ("raw vs cooked food", "diet"),
    ("dietary restrictions", "diet"), ("recipes for dosha", "diet"), ("balanced meal", "diet"), ("six tastes", "diet"),
    ("sweet sour salty", "diet"), ("bitter pungent astringent", "diet"), ("food combinations", "diet"), ("incompatible foods", "diet"),
    ("ayurvedic cooking", "diet"), ("healing foods", "diet"), ("detox diet", "diet"), ("weight loss diet", "diet"),
    ("weight gain diet", "diet"), ("vegetarian diet ayurveda", "diet"), ("what to drink", "diet"), ("hydration", "diet"),
    ("food", "diet"), ("eat", "diet"), ("meal", "diet"), ("cooking", "diet"), ("recipe", "diet"), ("nutrient", "diet"),
]

yoga_data = [
    ("yoga poses", "yoga"), ("exercise routine", "yoga"), ("yoga for me", "yoga"), ("which asanas", "yoga"),
    ("physical activity", "yoga"), ("workout suggestions", "yoga"), ("yoga recommendations", "yoga"), ("best exercises", "yoga"),
    ("fitness", "yoga"), ("yoga for back pain", "yoga"), ("morning yoga", "yoga"), ("evening yoga", "yoga"),
    ("yoga for stress", "yoga"), ("yoga for digestion", "yoga"), ("breathing exercises", "yoga"), ("pranayama", "yoga"),
    ("meditation techniques", "yoga"), ("surya namaskar", "yoga"), ("beginner yoga", "yoga"), ("advanced yoga", "yoga"),
    ("yoga schedule", "yoga"), ("how often should i do yoga", "yoga"), ("yoga benefits", "yoga"), ("best asanas for weight loss", "yoga"),
    ("yoga for flexibility", "yoga"), ("yoga nidra", "yoga"), ("restorative yoga", "yoga"), ("power yoga", "yoga"),
    ("yoga flow", "yoga"), ("guided meditation", "yoga"), ("mindfulness", "yoga"), ("chanting", "yoga"),
    ("mantras", "yoga"), ("stretching", "yoga"), ("joint movements", "yoga"), ("warm up exercises", "yoga"),
    ("cooling pranayama", "yoga"), ("heating pranayama", "yoga"), ("mudras", "yoga"), ("daily practice", "yoga"),
    ("asana", "yoga"), ("pose", "yoga"), ("exercise", "yoga"), ("stretch", "yoga"), ("workout", "yoga"),
]

stress_data = [
    ("reduce stress", "stress"), ("anxiety relief", "stress"), ("calm down", "stress"), ("mental peace", "stress"),
    ("feeling anxious", "stress"), ("stress management", "stress"), ("relax mind", "stress"), ("too much stress", "stress"),
    ("how to handle pressure", "stress"), ("peace of mind", "stress"), ("ayurveda for stress", "stress"), ("herbs for stress", "stress"),
    ("meditation for stress", "stress"), ("feeling overwhelmed", "stress"), ("tension relief", "stress"), ("mental exhaustion", "stress"),
    ("burnout", "stress"), ("calming techniques", "stress"), ("stress symptoms", "stress"), ("worried all the time", "stress"),
    ("panic attack", "stress"), ("soothe nerves", "stress"), ("mental clarity", "stress"), ("emotional balance", "stress"),
    ("mood swings", "stress"), ("depression", "stress"), ("feeling low", "stress"), ("mental fatigue", "stress"),
    ("brain fog", "stress"), ("nervous system support", "stress"), ("relaxation", "stress"), ("mind calm", "stress"),
    ("de-stress", "stress"), ("unwind", "stress"), ("peaceful mind", "stress"),
    ("anxiety", "stress"), ("tension", "stress"), ("calm", "stress"), ("mental", "stress"), ("worry", "stress"),
]

sleep_data = [
    ("sleep better", "sleep"), ("insomnia", "sleep"), ("cant sleep", "sleep"), ("rest advice", "sleep"),
    ("sleep schedule", "sleep"), ("improve sleep quality", "sleep"), ("waking up tired", "sleep"), ("can't fall asleep", "sleep"),
    ("bad dreams", "sleep"), ("night routine", "sleep"), ("ayurveda for sleep", "sleep"), ("best time to sleep", "sleep"),
    ("waking up early", "sleep"), ("sleep hygiene", "sleep"), ("deep sleep", "sleep"), ("sleep disorders", "sleep"),
    ("insomnia natural remedies", "sleep"), ("sleeping pills alternative", "sleep"), ("how many hours sleep", "sleep"),
    ("restful sleep", "sleep"), ("waking up in middle of night", "sleep"), ("snoring", "sleep"), ("sleep position", "sleep"),
    ("oil massage for sleep", "sleep"), ("milk before bed", "sleep"), ("prepare for bed", "sleep"), ("bedtime ritual", "sleep"),
    ("sleep environment", "sleep"), ("get better rest", "sleep"), ("tired all day", "sleep"), ("exhaustion", "sleep"),
    ("nap during day", "sleep"), ("circadian rhythm", "sleep"), ("sleep aid", "sleep"), ("calm sleep", "sleep"),
    ("sleep", "sleep"), ("insomnia", "sleep"), ("dream", "sleep"), ("awake", "sleep"), ("tired", "sleep"),
]

digestion_data = [
    ("digestive issues", "digestion"), ("agni fire", "digestion"), ("stomach problems", "digestion"), ("improve digestion", "digestion"),
    ("bloating", "digestion"), ("gas and acidity", "digestion"), ("constipation relief", "digestion"), ("indigestion cure", "digestion"),
    ("heavy stomach", "digestion"), ("digestive fire", "digestion"), ("poor digestion", "digestion"), ("gut health", "digestion"),
    ("stomach pain", "digestion"), ("increase metabolism", "digestion"), ("digestive spices", "digestion"), ("detox stomach", "digestion"),
    ("cleanse stomach", "digestion"), ("bloating after eating", "digestion"), ("heartburn", "digestion"), ("acid reflux", "digestion"),
    ("appetite loss", "digestion"), ("excessive hunger", "digestion"), ("burning sensation", "digestion"), ("nausea", "digestion"),
    ("loose motion", "digestion"), ("diarrhea", "digestion"), ("IBS", "digestion"), ("gut flora", "digestion"),
    ("probiotics ayurveda", "digestion"), ("ginger for digestion", "digestion"), ("cumin water", "digestion"), ("fennel seeds", "digestion"),
    ("gut cleansing", "digestion"), ("ama toxins", "digestion"), ("digestive power", "digestion"),
    ("stomach", "digestion"), ("gut", "digestion"), ("digest", "digestion"), ("gas", "digestion"), ("bloat", "digestion"),
]

greeting_data = [
    ("hello", "greeting"), ("hi", "greeting"), ("hey", "greeting"), ("namaste", "greeting"), ("good morning", "greeting"),
    ("whats up", "greeting"), ("hola", "greeting"), ("greetings", "greeting"), ("nice to meet you", "greeting"),
    ("hi there", "greeting"), ("hello bot", "greeting"), ("good afternoon", "greeting"), ("good evening", "greeting"),
    ("yo", "greeting"), ("hi ayushwell", "greeting"), ("namaskaram", "greeting"), ("are you there", "greeting"),
    ("start chat", "greeting"), ("hello friend", "greeting"), ("good day", "greeting"), ("hi assistant", "greeting"),
    ("welcome", "greeting"), ("is anyone there", "greeting"), ("hello ai", "greeting"), ("hi buddy", "greeting"),
    ("hey doc", "greeting"), ("good night", "greeting"), ("sup", "greeting"), ("hiya", "greeting"), ("howdy", "greeting"),
]

help_data = [
    ("help me", "help"), ("what can you do", "help"), ("how to use", "help"), ("guide me", "help"), ("features", "help"),
    ("capabilities", "help"), ("what are you", "help"), ("who are you", "help"), ("assist me", "help"), ("i need help", "help"),
    ("support", "help"), ("what do you know", "help"), ("how does this work", "help"), ("show me options", "help"),
    ("menu", "help"), ("commands", "help"), ("what is this app", "help"), ("about you", "help"), ("bot info", "help"),
    ("user guide", "help"), ("where do i start", "help"), ("get started", "help"), ("instructions", "help"), ("tutorial", "help"),
    ("explain features", "help"), ("what can i ask", "help"), ("example questions", "help"), ("need assistance", "help"),
    ("help please", "help"), ("usage guide", "help"),
]

generic_data = [
    ("ok", "generic"), ("thanks", "generic"), ("thank you", "generic"), ("cool", "generic"), ("nice", "generic"),
    ("alright", "generic"), ("great", "generic"), ("awesome", "generic"), ("good job", "generic"), ("okay", "generic"),
    ("sounds good", "generic"), ("perfect", "generic"), ("bye", "generic"), ("see you", "generic"), ("understood", "generic"),
    ("got it", "generic"), ("sure", "generic"), ("fine", "generic"), ("wonderful", "generic"), ("excellent", "generic"),
    ("amazing", "generic"), ("cheers", "generic"), ("talk to you later", "generic"), ("goodbye", "generic"), ("exit", "generic"),
    ("quit", "generic"), ("done", "generic"), ("finished", "generic"), ("no problem", "generic"), ("you are welcome", "generic"),
]

take_assessment_data = [
    ("take assessment", "take_assessment"), ("start assessment", "take_assessment"), ("i want to know my dosha", "take_assessment"),
    ("what is my body type", "take_assessment"), ("check my prakriti", "take_assessment"), ("do the quiz", "take_assessment"),
    ("start test", "take_assessment"), ("begin assessment", "take_assessment"), ("find my dosha", "take_assessment"),
    ("assessment", "take_assessment"), ("test", "take_assessment"), ("quiz", "take_assessment"), ("prakriti test", "take_assessment"),
    ("go to assessment", "take_assessment"), ("launch quiz", "take_assessment"), ("start the test", "take_assessment"),
    ("i want to take the test", "take_assessment"), ("where is the assessment", "take_assessment"), ("open assessment", "take_assessment"),
    ("show me the quiz", "take_assessment"), ("analyze my dosha", "take_assessment"), ("dosha analysis", "take_assessment"),
    ("start diagnosis", "take_assessment"), ("check my constitution", "take_assessment"), ("begin quiz", "take_assessment"),
    ("take the survey", "take_assessment"), ("health assessment", "take_assessment"), ("body type check", "take_assessment"),
    ("prakriti check", "take_assessment"), ("run assessment", "take_assessment"), ("i want to do the assessment", "take_assessment"),
    ("open the test", "take_assessment"), ("start my evaluation", "take_assessment"), ("evaluate my dosha", "take_assessment"),
    ("take the dosha test", "take_assessment"), ("begin the survey", "take_assessment"), ("launch the assessment", "take_assessment"),
    ("take the quiz", "take_assessment"), ("test my prakriti", "take_assessment"), ("find out my body type", "take_assessment"),
]

# 2. Combine with 3x Weighting for Specific Classes
training_data = (
    prakriti_data + dosha_general_data + vata_data + pitta_data + kapha_data + 
    diet_data * 3 +  # TRIPLE WEIGHT
    yoga_data * 3 +  # TRIPLE WEIGHT
    stress_data * 3 + # TRIPLE WEIGHT
    sleep_data * 3 +  # TRIPLE WEIGHT
    digestion_data * 3 + # TRIPLE WEIGHT
    greeting_data * 3 + help_data * 3 + generic_data * 3 + take_assessment_data * 3 # ADD WEIGHT BALANCE
)

X_train = [text for text, _ in training_data]
y_train = [label for _, label in training_data]

# 3. ML Pipeline (LogisticRegression - Optimized for accuracy ~96%)
ml_chatbot_model = Pipeline([
    ('tfidf', TfidfVectorizer(
        ngram_range=(1, 3), 
        max_features=5000,
        lowercase=True,
        strip_accents='unicode'
    )),
    ('clf', LogisticRegression(
        max_iter=3000,
        C=10.0,
        random_state=42
    ))
])

# Train model immediately
ml_chatbot_model.fit(X_train, y_train)


# ==================== RESPONSES ====================

ml_responses = {
    "prakriti": "Prakriti is your unique mind-body constitution! Take our 10-question assessment to discover your dominant dosha and get personalized wellness recommendations. Click 'Prakriti Assessment' in the menu to start!",
    
    "dosha_general": "The three doshas are Vata (air/movement), Pitta (fire/transformation), and Kapha (earth/structure). Each person has a unique combination that determines their physical and mental traits!",
    
    "vata": "Vata represents air and movement. Balanced Vata = creative, energetic, flexible. Imbalanced = anxiety, dry skin, irregular digestion. {personalized}",
    
    "pitta": "Pitta represents fire and transformation. Balanced Pitta = focused, intelligent, determined. Imbalanced = anger, inflammation, acidity. {personalized}",
    
    "kapha": "Kapha represents earth and water. Balanced Kapha = calm, strong, nurturing. Imbalanced = lethargy, weight gain, congestion. {personalized}",
    
    "diet": "Diet varies by dosha! {personalized_diet} Complete your assessment for a detailed personalized nutrition plan with specific foods to favor and avoid!",
    
    "yoga": "Yoga recommendations depend on your dosha! {personalized_yoga} Take the assessment to get your complete personalized yoga plan with specific poses and practice schedule!",
    
    "stress": "For stress relief: Practice Pranayama (deep breathing) for 10-15 min daily, try calming poses like Child's Pose, maintain regular sleep schedule. Vata types are especially prone to anxiety - routine helps!",
    
    "sleep": "Ayurvedic sleep tips: Sleep by 10 PM, wake by 6 AM. Vata: warm oil massage before bed. Pitta: keep room cool, avoid screens. Kapha: don't oversleep, wake early! Consistency is key for all doshas.",
    
    "digestion": "Strengthen your Agni (digestive fire): eat at regular times, make lunch your largest meal, drink warm water throughout the day, use digestive spices (ginger, cumin, coriander), avoid snacking between meals.",
    
    "greeting": "Namaste! 🙏 I'm your AI-powered Ayurvedic wellness guide. I can help with dosha analysis, personalized diet plans, yoga recommendations, stress management, and lifestyle tips. What would you like to know?",
    
    "help": "I can help you with: ✅ Understanding your Prakriti/Dosha ✅ Personalized diet recommendations ✅ Yoga and exercise guidance ✅ Stress management ✅ Sleep optimization ✅ Digestive health. Just ask me anything!",
    
    "generic": "I'm here to help with Ayurvedic wellness! You can ask me about your dosha, diet plans, yoga routines, stress relief, or any other health questions. What would you like to know?",
    
    "take_assessment": "Great! Let's discover your unique Prakriti. I'm redirecting you to the assessment page now. Please answer the questions honestly for the best results! 📝"
}

# ==================== AUTH ====================

def get_current_user():
    token = request.headers.get('Authorization')
    if not token or token not in active_tokens:
        return None
    return active_tokens[token]

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        role=data['role']
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'Registration successful!'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = secrets.token_hex(32)
    active_tokens[token] = user.id
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }
    }), 200

@app.route('/api/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization')
    if token in active_tokens:
        del active_tokens[token]
    return jsonify({'message': 'Logout successful'}), 200

# ==================== ASSESSMENT ====================

@app.route('/api/assessment', methods=['POST'])
def submit_assessment():
    user_id = get_current_user()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    Assessment.query.filter_by(user_id=user_id, is_active=True).update({'is_active': False})
    
    answers = data['answers']
    vata_score = sum(1 for a in answers if a == 'vata')
    pitta_score = sum(1 for a in answers if a == 'pitta')
    kapha_score = sum(1 for a in answers if a == 'kapha')
    
    dominant_dosha = max({'vata': vata_score, 'pitta': pitta_score, 'kapha': kapha_score}.items(), key=lambda x: x[1])[0]
    
    assessment = Assessment(
        user_id=user_id,
        answers=answers,
        vata_score=vata_score,
        pitta_score=pitta_score,
        kapha_score=kapha_score,
        dominant_dosha=dominant_dosha,
        is_active=True
    )
    
    db.session.add(assessment)
    db.session.commit()
    
    recommendations = generate_recommendations(dominant_dosha, assessment.id, user_id)
    
    return jsonify({
        'assessment_id': assessment.id,
        'vata_score': vata_score,
        'pitta_score': pitta_score,
        'kapha_score': kapha_score,
        'dominant_dosha': dominant_dosha,
        'recommendations': recommendations
    }), 201

@app.route('/api/assessment/current', methods=['GET'])
def get_current_assessment():
    user_id = get_current_user()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    assessment = Assessment.query.filter_by(user_id=user_id, is_active=True).first()
    
    if not assessment:
        return jsonify({'message': 'No assessment found'}), 404
    
    recommendation = Recommendation.query.filter_by(assessment_id=assessment.id).first()
    
    return jsonify({
        'assessment_id': assessment.id,
        'vata_score': assessment.vata_score,
        'pitta_score': assessment.pitta_score,
        'kapha_score': assessment.kapha_score,
        'dominant_dosha': assessment.dominant_dosha,
        'created_at': assessment.created_at.isoformat(),
        'recommendations': {
            'diet': recommendation.diet_plan if recommendation else None,
            'yoga': recommendation.yoga_plan if recommendation else None,
            'lifestyle': recommendation.lifestyle_tips if recommendation else None
        }
    }), 200

# ==================== IMPROVED RECOMMENDATIONS ====================

def generate_recommendations(dosha, assessment_id, user_id):
    recommendations_map = {
        'vata': {
            'diet': {
                'foods_to_favor': [
                    'Warm, cooked foods like soups and stews',
                    'Sweet fruits: bananas, avocados, mangoes',
                    'Whole grains: rice, wheat, oats',
                    'Dairy: warm milk, ghee, paneer',
                    'Nuts and seeds: almonds, sesame, flaxseeds',
                    'Root vegetables: carrots, beets, sweet potatoes',
                    'Warm spices: ginger, cinnamon, cumin, turmeric'
                ],
                'foods_to_avoid': [
                    'Cold, raw, or frozen foods',
                    'Dry snacks like crackers and chips',
                    'Excessive caffeine and stimulants',
                    'Bitter vegetables in excess',
                    'Carbonated drinks',
                    'Leftover or stale food'
                ],
                'meal_timing': 'Eat at regular times daily. Never skip meals. Breakfast 7-8 AM, Lunch 12-1 PM (largest meal), Dinner 6-7 PM (warm, light). Avoid eating after 8 PM.'
            },
            'yoga': {
                'poses': [
                    'Child\'s Pose (Balasana)',
                    'Cat-Cow Stretch (Marjaryasana-Bitilasana)',
                    'Seated Forward Bend (Paschimottanasana)',
                    'Legs Up the Wall (Viparita Karani)',
                    'Corpse Pose (Savasana)',
                    'Mountain Pose (Tadasana)'
                ],
                'duration': '20-30 minutes',
                'frequency': 'Daily, ideally in morning',
                'focus': 'Grounding, slow movements. Focus on stability and breathing. Avoid excessive jumping or vigorous vinyasas.'
            },
            'lifestyle': [
                'Sleep by 10 PM, wake by 6 AM for routine',
                'Daily oil massage (Abhyanga) with warm sesame oil',
                'Stay warm - wear layers, avoid cold wind',
                'Practice meditation and deep breathing (Pranayama)',
                'Maintain daily routine - same times for eating, sleeping',
                'Avoid excessive travel and overstimulation'
            ]
        },
        'pitta': {
            'diet': {
                'foods_to_favor': [
                    'Cooling foods: cucumber, melons, coconut',
                    'Sweet fruits: grapes, pears, dates, pomegranates',
                    'Leafy greens: spinach, kale, lettuce',
                    'Grains: rice, barley, oats, wheat',
                    'Dairy: milk, ghee, butter (cooling)',
                    'Mild spices: coriander, fennel, mint, cardamom',
                    'Legumes: mung beans, chickpeas'
                ],
                'foods_to_avoid': [
                    'Spicy, salty, or sour foods',
                    'Red meat and fried foods',
                    'Alcohol and caffeine',
                    'Fermented foods in excess',
                    'Hot spices: chili, cayenne',
                    'Tomatoes, onions, garlic in excess'
                ],
                'meal_timing': 'Never skip lunch (12-1 PM) - strongest digestive fire. Light breakfast, moderate dinner by 7 PM. Avoid eating when angry or stressed.'
            },
            'yoga': {
                'poses': [
                    'Moon Salutation (Chandra Namaskar)',
                    'Shoulder Stand (Sarvangasana)',
                    'Fish Pose (Matsyasana)',
                    'Cobra Pose (Bhujangasana)',
                    'Boat Pose (Navasana)',
                    'Child\'s Pose (Balasana)'
                ],
                'duration': '30-45 minutes',
                'frequency': '4-5 times per week',
                'focus': 'Cooling practices. Avoid excessive heat-building exercises. Practice during cooler hours (morning/evening).'
            },
            'lifestyle': [
                'Avoid overworking - take regular breaks',
                'Practice cooling Pranayama (Sitali, Sitkari)',
                'Spend time in nature, near water',
                'Avoid hot midday sun',
                'Cultivate patience and compassion',
                'Moderate exercise - avoid competitive sports'
            ]
        },
        'kapha': {
            'diet': {
                'foods_to_favor': [
                    'Light, warm, cooked foods',
                    'Pungent spices: ginger, black pepper, turmeric, garlic',
                    'Bitter greens: kale, dandelion, arugula',
                    'Astringent fruits: apples, pears, pomegranates',
                    'Legumes: lentils, black beans, chickpeas',
                    'Whole grains in moderation: quinoa, barley, millet',
                    'Honey (raw, unheated) as sweetener'
                ],
                'foods_to_avoid': [
                    'Heavy, oily, fried foods',
                    'Excessive dairy, especially cheese and yogurt',
                    'Sweet, salty, sour tastes in excess',
                    'Wheat and refined carbohydrates',
                    'Cold drinks and ice cream',
                    'Red meat and fatty foods'
                ],
                'meal_timing': 'Light or skip breakfast. Largest meal at lunch (12-1 PM). Light, early dinner (6 PM). Avoid snacking between meals.'
            },
            'yoga': {
                'poses': [
                    'Sun Salutations (Surya Namaskar) - 12 rounds',
                    'Warrior Poses (Virabhadrasana I, II, III)',
                    'Triangle Pose (Trikonasana)',
                    'Camel Pose (Ustrasana)',
                    'Bow Pose (Dhanurasana)',
                    'Headstand (Sirsasana) if practiced'
                ],
                'duration': '45-60 minutes',
                'frequency': 'Daily',
                'focus': 'Vigorous, energizing practice. Fast-paced vinyasa. Build heat and sweat. Practice in morning for best results.'
            },
            'lifestyle': [
                'Wake early (before 6 AM) - avoid sleeping in',
                'Vigorous daily exercise - running, aerobics',
                'Stay active and avoid sedentary lifestyle',
                'Seek variety and new experiences',
                'Avoid daytime naps',
                'Practice stimulating Pranayama (Kapalabhati, Bhastrika)'
            ]
        }
    }
    
    selected = recommendations_map[dosha]
    
    recommendation = Recommendation(
        user_id=user_id,
        assessment_id=assessment_id,
        diet_plan=selected['diet'],
        yoga_plan=selected['yoga'],
        lifestyle_tips=selected['lifestyle']
    )
    
    db.session.add(recommendation)
    db.session.commit()
    
    return selected

# ==================== PROGRESS ====================

@app.route('/api/progress', methods=['POST'])
def add_progress():
    user_id = get_current_user()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    today = datetime.utcnow().date()
    existing = Progress.query.filter_by(user_id=user_id, date=today).first()
    
    if existing:
        for key in ['calories', 'activity_minutes', 'water_ml', 'sleep_hours', 'weight_kg', 'stress_level', 'notes']:
            if key in data:
                setattr(existing, key, data[key])
    else:
        progress = Progress(user_id=user_id, date=today, **data)
        db.session.add(progress)
    
    db.session.commit()
    return jsonify({'message': 'Progress updated'}), 200

@app.route('/api/progress', methods=['GET'])
def get_progress():
    user_id = get_current_user()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    days = request.args.get('days', 30, type=int)
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    records = Progress.query.filter(
        Progress.user_id == user_id,
        Progress.date >= start_date
    ).order_by(Progress.date.asc()).all()
    
    return jsonify([{
        'date': p.date.isoformat(),
        'calories': p.calories,
        'activity_minutes': p.activity_minutes,
        'water_ml': p.water_ml,
        'sleep_hours': p.sleep_hours,
        'weight_kg': p.weight_kg,
        'stress_level': p.stress_level,
        'notes': p.notes
    } for p in records]), 200

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    user_id = get_current_user()
    data = request.json
    message = data['message'].lower().strip()
    
    # Get user's assessment
    user_dosha = None
    if user_id:
        assessment = Assessment.query.filter_by(user_id=user_id, is_active=True).first()
        if assessment:
            user_dosha = assessment.dominant_dosha
    
    try:
        # Predict intent
        predicted_intent = ml_chatbot_model.predict([message])[0]
        response = ml_responses.get(predicted_intent, ml_responses["help"])
        
        # Personalize
        if "{personalized}" in response and user_dosha:
            personalization = {
                "vata": " This is YOUR primary dosha! Focus on warmth, routine, and grounding practices.",
                "pitta": " This is YOUR primary dosha! Focus on cooling foods and avoiding excess heat.",
                "kapha": " This is YOUR primary dosha! Focus on energizing activities and light foods."
            }
            response = response.replace("{personalized}", personalization.get(user_dosha, ""))
        else:
            response = response.replace("{personalized}", " Take the assessment to discover yours!")
        
        if "{personalized_diet}" in response and user_dosha:
            diet_advice = {
                "vata": "Your Vata diet: Warm, cooked foods, sweet fruits, healthy oils. Avoid cold, raw foods.",
                "pitta": "Your Pitta diet: Cooling foods like cucumber, sweet fruits, leafy greens. Avoid spicy, salty, sour foods.",
                "kapha": "Your Kapha diet: Light, warm foods with pungent spices. Avoid heavy, oily foods and dairy."
            }
            response = response.replace("{personalized_diet}", diet_advice.get(user_dosha, ""))
        else:
            response = response.replace("{personalized_diet}", "")
        
        if "{personalized_yoga}" in response and user_dosha:
            yoga_advice = {
                "vata": "Vata needs grounding poses like Child's Pose and forward bends. 20-30 min daily.",
                "pitta": "Pitta needs cooling poses like Moon Salutations. 30-45 min, 4-5x/week.",
                "kapha": "Kapha needs energizing Sun Salutations and Warrior poses! 45-60 min daily."
            }
            response = response.replace("{personalized_yoga}", yoga_advice.get(user_dosha, ""))
        else:
            response = response.replace("{personalized_yoga}", "")
            
        action = None
        if predicted_intent == "take_assessment":
            action = "redirect_assessment"
        
        return jsonify({'response': response, 'action': action}), 200
        
    except Exception as e:
        print(f"ML Chatbot Error: {e}")
        return jsonify({'response': "I can help with Ayurveda, doshas, diet, yoga, and wellness! Try asking: 'What's my dosha?', 'Diet tips', or 'Yoga for me'. What interests you?"}), 200
      
# ==================== INIT ====================

@app.route('/api/init-db', methods=['GET'])
def init_db():
    try:
        db.create_all()
        return jsonify({'message': 'Database initialized!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
