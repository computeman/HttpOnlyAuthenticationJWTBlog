from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
)
from functools import wraps

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this in production
jwt = JWTManager(app)
CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5173", "http://localhost:5173"])

# Mock user data
USERS = {"user": "password"}

def cookie_jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except:
            token = request.cookies.get('access_token')
            if not token:
                return jsonify({"message": "Missing token"}), 401
            try:
                verify_jwt_in_request(lambda: token)
            except Exception as e:
                return jsonify({"message": str(e)}), 401
        return fn(*args, **kwargs)
    return wrapper

@app.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if USERS.get(username) == password:
        access_token = create_access_token(identity=username)
        response = jsonify({"message": "Login successful"})
        response.set_cookie('access_token', access_token, secure=True, httponly=True, samesite='None')
        return response
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/protected', methods=['GET'])
# @cross_origin(supports_credentials=True)
@cookie_jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"This is a protected route for {current_user}"}), 200

if __name__ == '__main__':
    app.run(debug=True)
