from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(
    dotenv_path=".env",
)
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
import os

app = Flask(__name__, template_folder='templates')
CORS(app)

# Load your OpenAI API key

# Load the feedback prompt
with open("prompts/feedback_prompt.txt", "r") as file:
    feedback_prompt = file.read()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    conversation = data.get('conversation', [])

    if not conversation:
        return jsonify({"error": "No conversation provided."}), 400

    try:
        # Build the messages for OpenAI API
        messages = [{"role": "system", "content": feedback_prompt}] + conversation

        response = client.chat.completions.create(model="gpt-4",
        messages=messages,
        max_tokens=150,
        temperature=0.7)

        reply = response.choices[0].message.content.strip()

        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8001)