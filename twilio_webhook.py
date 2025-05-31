from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get('Body', '')
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You help users in South Africa find car parts. Ask for vehicle make/model/year, part needed, urgency, location, and contact info."},
            {"role": "user", "content": incoming_msg}
        ]
    )

    reply = response['choices'][0]['message']['content']
    twilio_response = MessagingResponse()
    twilio_response.message(reply)
    return str(twilio_response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
