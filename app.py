from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message')
        rasa_url = "http://localhost:5005/webhooks/rest/webhook"
        payload = {
            "sender": "user",
            "message": user_message
        }
        
        response = requests.post(rasa_url, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        
        response_data = response.json()
        
        if response_data:
            bot_response = response_data[0].get('text', "Sorry, I didn't get that. Could you please rephrase?")
        else:
            bot_response = "Sorry, I didn't get that. Could you please rephrase?"
    
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        bot_response = "Sorry, there was an error communicating with the Rasa server."
    
    except ValueError:
        print("ValueError: Invalid JSON response from Rasa server")
        bot_response = "Sorry, there was an error processing the response from the Rasa server."
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)

