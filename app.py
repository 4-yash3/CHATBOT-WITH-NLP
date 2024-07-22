from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='D:/RASA/src/templates')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    rasa_url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {
        "sender": "user",
        "message": user_message
    }
    response = requests.post(rasa_url, json=payload)
    response_data = response.json()
    if response_data:
        bot_response = response_data[0]['text']
    else:
        bot_response = "Sorry, I didn't get that. Could you please rephrase?"
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)


