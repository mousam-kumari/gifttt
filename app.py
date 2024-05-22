from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Your Gemini API key
GEMINI_API_KEY = 'AIzaSyCclRMJ0cdftV0xAhHS7yPEyMWbc3TZtPs'

# Initialize the Gemini API client
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.0-pro')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_gift_idea', methods=['POST'])
def generate_gift_idea():
    data = request.json
    age = data.get('age')
    gender = data.get('gender')
    occasion = data.get('occasion')
    recipient_type = data.get('recipient_type')
    categories = data.get('categories')
    prompt = f"Suggest 12 unique and highly-rated gift ideas for a {age}-year-old {recipient_type} who is {gender} and loves {categories}. The occasion is {occasion}. Please include specific product names that can be bought on Amazon India."

    # Generate gift ideas using the Gemini API
    try:
      response = model.generate_content(prompt)
      generated_text = response.text
      gift_ideas = process_text_for_gift_ideas(generated_text)[:12]  # Get only 12 ideas
      return jsonify({"gift_ideas": gift_ideas})  # Get only 5 ideas
    except Exception as e:
      print(f"Error generating gift ideas: {e}")
      return jsonify({"error": "Error generating gift ideas"}), 500
@app.route('/search_gift_idea', methods=['POST'])
def search_gift_idea():
    data = request.json
    prompt = data.get('prompt')

    # Generate gift ideas using the Gemini API based on the search prompt
    try:
        response = model.generate_content(prompt)
        generated_text = response.text
        gift_ideas = process_text_for_gift_ideas(generated_text)[:12]  # Get only 12 ideas
        return jsonify({"gift_ideas": gift_ideas})
    except Exception as e:
        print(f"Error generating gift ideas: {e}")
        return jsonify({"error": "Error generating gift ideas"}), 500



def process_text_for_gift_ideas(text):
    return text.split('\n')[:12]  

if __name__ == '__main__':
    app.run(debug=True)
