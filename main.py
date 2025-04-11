# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# import joblib
# from alert import send_alert  # Import the send_alert function
# import bleach
# import time  # To manage blocking duration

# app = FastAPI()

# origins = [
#     "http://localhost:3000",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Load the pre-trained model and vectorizer
# model = joblib.load("xgboost_model.pkl")
# vectorizer = joblib.load("tfidf_vectorizer.pkl")

# # Dictionary to store blocked IPs with unblock time
# blocked_ips = {}
# #BLOCK_DURATION = 1 * 60  # Block duration in seconds (e.g., 15 minutes)

# def is_ip_blocked(ip):
#     """Check if IP is currently blocked."""
#     unblock_time = blocked_ips.get(ip)
#     if unblock_time and time.time() < unblock_time:
#         return True
#     # Unblock IP if time has expired
#     if unblock_time and time.time() >= unblock_time:
#         del blocked_ips[ip]
#     return False

# @app.post("/predict")
# async def predict(input_text: dict, request: Request):
#     # Get attacker's IP address
#     attacker_ip = request.client.host
    
#     # Check if the IP is blocked
#     if is_ip_blocked(attacker_ip):
#         return {"error": "Your IP has been temporarily blocked due to previous malicious activity."}

#     input_text_value = bleach.clean(input_text.get("input"))
#     if not input_text_value:
#         return {"error": "No input provided"}

#     # Vectorize the input and make a prediction
#     vectorized_input = vectorizer.transform([input_text_value])
#     prediction = model.predict(vectorized_input)

#     # Determine if the input is malicious
#     result = "malicious" if prediction[0] == 1 else "not malicious"
    
#     # Send alert and block IP if malicious
#     if result == "malicious":
#         user_agent = request.headers.get("user-agent")
#         send_alert(input_text_value, attacker_ip, user_agent)
#         # Block the IP
#         #blocked_ips[attacker_ip] = time.time() + BLOCK_DURATION  # Set unblock time
#         print(result)
#         return {"result": result}
    
#     return {"result": result}

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the Malicious Input Detection API!"}


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import joblib
import bleach
import time
from alert import send_alert  # Your custom alert module

app = FastAPI()

# Allow frontend requests from this origin
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load XGBoost model and TF-IDF vectorizer
model = joblib.load("xgboost_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# IP blocking dictionary
blocked_ips = {}
BLOCK_DURATION = 0 * 60  # seconds

def is_ip_blocked(ip):
    unblock_time = blocked_ips.get(ip)
    if unblock_time and time.time() < unblock_time:
        return True
    if unblock_time and time.time() >= unblock_time:
        del blocked_ips[ip]
    return False

@app.post("/predict")
async def predict(input_text: dict, request: Request):
    attacker_ip = request.client.host

    # Check if IP is blocked
    if is_ip_blocked(attacker_ip):
        return {"error": "Your IP has been temporarily blocked due to previous malicious activity."}

    clean_input = bleach.clean(input_text.get("input", ""))
    if not clean_input:
        return {"error": "No input provided"}

    # Vectorize input and predict
    vectorized_input = vectorizer.transform([clean_input])
    prediction = model.predict(vectorized_input)
    result = "malicious" if prediction[0] == 1 else "not malicious"

    if result == "malicious":
        user_agent = request.headers.get("user-agent")
        send_alert(clean_input, attacker_ip, user_agent)
        # Uncomment below to enable IP blocking
        # blocked_ips[attacker_ip] = time.time() + BLOCK_DURATION
        print(f"Malicious input detected from {attacker_ip}")

    return {"result": result}

@app.get("/")
async def root():
    return {"message": "Welcome to the Malicious Input Detection API powered by XGBoost!"}

