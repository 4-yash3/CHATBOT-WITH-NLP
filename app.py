from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('D:\RASA\CHATBOT-WITH-NLP\Tempelate\index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"sender": "user", "message": user_message})
    response_text = response.json()
    if response_text:
        return jsonify({"response": response_text[0]["text"]})
    return jsonify({"response": "Sorry, I didn't get that. Could you please rephrase?"})

if __name__ == '__main__':
    app.run(debug=True)

