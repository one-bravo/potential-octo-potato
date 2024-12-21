from flask import Flask, request, jsonify, send_from_directory, render_template
from anthropic import Anthropic
import os
from datetime import datetime
import json

app = Flask(__name__)
anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

@app.route('/')
def serve_app():
    return render_template('index.html')

@app.route('/forecast', methods=['POST'])
def get_forecast():
    data = request.json
    
    # Format the user's answers into a meaningful prompt
    birthday = datetime.strptime(data['birthday'], '%Y-%m-%d')
    zodiac_sign = get_zodiac_sign(birthday)
    
    prompt = f"""You are a wise and insightful mystical guide who provides thoughtful, positive guidance. 
    Based on the following information about a person, provide a meaningful and uplifting 3-month forecast 
    that offers genuine insight while remaining open to interpretation. The forecast should be specific 
    enough to feel personal but universal enough to be widely applicable.

    Their details:
    - Birth Date: {birthday.strftime('%B %d')} (Zodiac: {zodiac_sign})
    - Preferred Environment: {data['environment']}
    - Peak Time of Day: {data['time']}
    - Resonant Element: {data['element']}
    - Mythical Companion: {data['creature']}
    - Energy Color: {data['color']}
    - Spirit Season: {data['season']}
    - Journey Type: {data['journey']}

    Provide a 3-paragraph forecast where:
    1. First paragraph covers the immediate month ahead
    2. Second paragraph covers the following month
    3. Third paragraph covers the third month
    
    Make each prediction meaningful, specific, and actionable while maintaining an air of mystery.
    Focus on growth, opportunities, and positive potential while acknowledging possible challenges.
    Use metaphorical language that connects to their chosen answers.
    Keep the tone mystical but grounded, and absolutely avoid generic horoscope clichés."""

    try:
        response = anthropic.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0.7,
            system="You are a wise and insightful mystical guide who provides thoughtful, positive guidance.",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return jsonify({"forecast": response.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_zodiac_sign(birthday):
    day = birthday.day
    month = birthday.month
    
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    else:
        return "Pisces"

if __name__ == '__main__':
    app.run(debug=False)
