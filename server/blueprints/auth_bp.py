from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import get_db
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    db = get_db()
    users = db.users

    if users.find_one({"email": email}):
        return jsonify({"msg": "User already exists"}), 409

    hashed_password = generate_password_hash(password)
    
    user_id = users.insert_one({
        "email": email,
        "password_hash": hashed_password,
        "name": name,
        "created_at": datetime.utcnow(),
        "profile": {
            "name": name,
            "age": None,
            "sex": None,
            "weight_kg": None,
            "height_cm": None,
            "conditions": []
        }
    }).inserted_id

    return jsonify({"msg": "User created successfully", "user_id": str(user_id)}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    db = get_db()
    user = db.users.find_one({"email": email})

    if user and check_password_hash(user['password_hash'], password):
        access_token = create_access_token(identity=str(user['_id']))
        refresh_token = create_refresh_token(identity=str(user['_id']))
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": str(user['_id']),
                "email": user['email'],
                "name": user.get('name')
            }
        }), 200

    return jsonify({"msg": "Invalid email or password"}), 401

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    db = get_db()
    user = db.users.find_one({"_id": current_user_id}) # Note: string/ObjectId conversion needed in practice
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
        
    return jsonify({
        "email": user['email'],
        "name": user.get('name'),
        "profile": user.get('profile')
    }), 200
