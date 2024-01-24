from flask import Flask, request, jsonify, session
from flask_session import Session
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Create a new instance of a ChatBot
bot = ChatBot("ChatterBot",
              storage_adapter='chatterbot.storage.SQLStorageAdapter',
              database_uri='sqlite:////Users/soorajjayasundaram/projects/chatbot/database.sqlite3'
    )

# Train the chatbot if the database is empty
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english")

@app.route('/message', methods=['POST'])
@cross_origin(supports_credentials=True)
def receive_message():
    data = request.json
    user_message = data.get('message')

    # Initialize a new conversation
    if 'conversation_id' not in session:
        session['conversation_id'] = str(os.urandom(16))

    # Retrieve the conversation object using the session's conversation_id
    conversation_id = session['conversation_id']
    bot_response = bot.get_response(user_message, conversation_id=conversation_id).text

    return jsonify({'text': bot_response})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
