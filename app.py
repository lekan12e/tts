import pyttsx3
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

engine = pyttsx3.init()

def speak_name(name):
    try:
        # Ensure the engine doesn't try to speak while it's already speaking
        engine.say(f"Hello, {name}!")
        engine.runAndWait()
    except RuntimeError as e:
        print(f"Error: {e}")

@app.route('/say-hello', methods=['POST'])
def say_hello():
    data = request.get_json()
    name = data.get('name')

    if name:
        # Start a thread to handle the speech without blocking the main thread
        thread = threading.Thread(target=speak_name, args=(name,))
        thread.start()

        return jsonify({"message": f"Hello, {name}!"}), 200
    else:
        return jsonify({"error": "Name not provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
