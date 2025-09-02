from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MySQL Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'your_username',  # Change this
    'password': 'your_password',  # Change this
    'database': 'mood_journal'
}

# Hugging Face API Simulation (Replace with actual API call)
def analyze_emotions_simulation(text):
    # This is a simulation - replace with actual Hugging Face API call
    # For real implementation, you would use:
    # from transformers import pipeline
    # emotion_classifier = pipeline('text-classification', model='j-hartmann/emotion-english-distilroberta-base', return_all_scores=True)
    # emotions = emotion_classifier(text)
    
    # Simulated emotion analysis based on keywords
    text_lower = text.lower()
    emotions = {
        'happy': 0,
        'sad': 0,
        'angry': 0,
        'surprise': 0,
        'fear': 0,
        'love': 0
    }
    
    # Simple keyword-based emotion detection (replace with AI model)
    happy_words = ['happy', 'joy', 'excited', 'good', 'great', 'wonderful', 'love', 'loved', 'awesome']
    sad_words = ['sad', 'unhappy', 'depressed', 'miserable', 'cry', 'crying', 'tears']
    angry_words = ['angry', 'mad', 'frustrated', 'annoyed', 'hate', 'hated']
    surprise_words = ['surprise', 'surprised', 'amazed', 'wow', 'unexpected']
    fear_words = ['scared', 'afraid', 'fear', 'fearful', 'anxious', 'anxiety', 'worry', 'worried']
    love_words = ['love', 'loved', 'adore', 'adored', 'care', 'caring', 'affection']
    
    # Count occurrences of emotion words
    for word in happy_words:
        emotions['happy'] += text_lower.count(word) * 10
        
    for word in sad_words:
        emotions['sad'] += text_lower.count(word) * 10
        
    for word in angry_words:
        emotions['angry'] += text_lower.count(word) * 10
        
    for word in surprise_words:
        emotions['surprise'] += text_lower.count(word) * 10
        
    for word in fear_words:
        emotions['fear'] += text_lower.count(word) * 10
        
    for word in love_words:
        emotions['love'] += text_lower.count(word) * 10
    
    # Ensure values are between 0 and 100
    for emotion in emotions:
        emotions[emotion] = min(100, emotions[emotion])
        emotions[emotion] = max(0, emotions[emotion])
    
    # If no emotions detected, provide default values
    if sum(emotions.values()) == 0:
        emotions = {
            'happy': 30,
            'sad': 20,
            'angry': 10,
            'surprise': 15,
            'fear': 15,
            'love': 10
        }
    
    return emotions

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({'status': 'ok', 'message': 'Backend is running'})

@app.route('/api/analyze', methods=['POST'])
def analyze_emotion():
    try:
        data = request.get_json()
        journal_text = data.get('text', '')
        
        if not journal_text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Analyze emotions (simulation)
        emotions = analyze_emotions_simulation(journal_text)
        
        # Connect to MySQL
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        # Insert into database
        query = """INSERT INTO journal_entries 
                 (entry_text, happy, sad, angry, surprise, fear, love) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        
        values = (
            journal_text,
            emotions['happy'],
            emotions['sad'],
            emotions['angry'],
            emotions['surprise'],
            emotions['fear'],
            emotions['love']
        )
        
        cursor.execute(query, values)
        connection.commit()
        
        # Get the inserted ID
        entry_id = cursor.lastrowid
        
        cursor.close()
        connection.close()
        
        return jsonify(emotions)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/entries', methods=['GET'])
def get_entries():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM journal_entries ORDER BY created_at DESC")
        entries = cursor.fetchall()
        
        # Convert datetime objects to strings
        for entry in entries:
            if 'created_at' in entry and isinstance(entry['created_at'], datetime):
                entry['created_at'] = entry['created_at'].isoformat()
        
        cursor.close()
        connection.close()
        
        return jsonify(entries)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)