from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

# Load the trained model and vectorizer
model = joblib.load('logistic_regression_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_text = data.get('input')
    if not input_text:
        return jsonify({'error': 'No input provided'}), 400

    # Vectorize the input text
    vectorized_input = vectorizer.transform([input_text])
    prediction = model.predict(vectorized_input)

    # Return the result
    result = 'malicious' if prediction[0] == 1 else 'not malicious'
    return jsonify({'result': result})

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Method Not Allowed', 'message': str(e.description)}), 405

@app.route('/')
def home():
    return 'Welcome to the Malicious Input Detection API! Use the /predict endpoint to test inputs.'

if __name__ == '__main__':
    app.run(debug=True)
