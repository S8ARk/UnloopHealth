from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.database import db_instance
from datetime import datetime

tracker_bp = Blueprint('tracker', __name__)

@tracker_bp.route('/search', methods=['GET'])
@jwt_required()
def search_foods():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    # Simple case-insensitive search in 'foods' collection
    foods = list(db_instance.get_collection('foods').find(
        {"name": {"$regex": query, "$options": "i"}},
        {"_id": 0}
    ).limit(10))
    
    return jsonify(foods), 200

@tracker_bp.route('/meal', methods=['POST'])
@jwt_required()
def log_meal():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # data should have food_name, calories, protein, carbs, fats
    log_entry = {
        "user_id": user_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now(),
        **data
    }
    
    db_instance.get_collection('meal_logs').insert_one(log_entry)
    return jsonify({"msg": "Meal logged"}), 201

@tracker_bp.route('/day', methods=['GET'])
@jwt_required()
def get_daily_summary():
    user_id = get_jwt_identity()
    today = datetime.now().strftime("%Y-%m-%d")
    
    logs = list(db_instance.get_collection('meal_logs').find(
        {"user_id": user_id, "date": today}
    ))
    
    summary = {
        "calories": sum(l.get('calories', 0) for l in logs),
        "protein": sum(l.get('protein', 0) for l in logs),
        "carbs": sum(l.get('carbs', 0) for l in logs),
        "fats": sum(l.get('fats', 0) for l in logs),
        "meals": [{ "name": l['name'], "calories": l['calories'] } for l in logs]
    }
    
    return jsonify(summary), 200
