from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# BASE DATA (Cleaned)
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

# TARGETED CLASSES - TRIPLE WEIGHTED
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
    # Reinforcement
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
    # Reinforcement
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
    # Reinforcement
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
    # Reinforcement
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
    # Reinforcement
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

training_data = (
    prakriti_data + dosha_general_data + vata_data + pitta_data + kapha_data + 
    diet_data * 3 +  # RESTORE TRIPLE WEIGHT
    yoga_data * 3 +  # RESTORE TRIPLE WEIGHT
    stress_data * 3 + # RESTORE TRIPLE WEIGHT
    sleep_data * 3 +  # RESTORE TRIPLE WEIGHT
    digestion_data * 3 + # RESTORE TRIPLE WEIGHT
    greeting_data * 3 + help_data * 3 + generic_data * 3 + take_assessment_data * 3 # ADD WEIGHT TO SOCIAL CLASSES
)

X = [text for text, _ in training_data]
y = [label for _, label in training_data]

# ML Pipeline (LogisticRegression handles weighted data well via probas)
pipeline = Pipeline([
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

# Split and Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=42)
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Current Accuracy: {accuracy * 100:.2f}%")
print(f"Test Set Size: {len(X_test)}")
print(f"Wrong Predictions:")
wrong_indices = [i for i in range(len(y_test)) if y_test[i] != y_pred[i]]
for i in wrong_indices:
    print(f"Text: '{X_test[i]}' | True: {y_test[i]} | Pred: {y_pred[i]}")
