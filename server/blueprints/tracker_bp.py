from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.database import db_instance
from datetime import datetime
from bson.objectid import ObjectId

tracker_bp = Blueprint('tracker', __name__)

@tracker_bp.route('/search', methods=['GET'])
@jwt_required()
def search_foods():
    query = request.args.get('q', '')
    diet = request.args.get('diet', 'All')
    
    if not query:
        return jsonify([])
    
    mongo_query = {"name": {"$regex": query, "$options": "i"}}
    if diet and diet != 'All':
        mongo_query["dietType"] = diet
        
    foods = list(db_instance.get_collection('foods').find(
        mongo_query,
        {"_id": 0}
    ).limit(10))
    
    return jsonify(foods), 200

@tracker_bp.route('/meal', methods=['POST'])
@jwt_required()
def log_meal():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    log_entry = {
        "user_id": user_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now(),
        "meal_type": data.get("meal_type", "Snacks"),
        "name": data.get("name", "Unknown Food"),
        "calories": float(data.get("calories", 0)),
        "protein": float(data.get("protein", 0)),
        "carbs": float(data.get("carbs", 0)),
        "fats": float(data.get("fats", 0))
    }
    
    db_instance.get_collection('meal_logs').insert_one(log_entry)
    return jsonify({"msg": "Meal logged"}), 201

@tracker_bp.route('/meal/<meal_id>', methods=['DELETE'])
@jwt_required()
def delete_meal(meal_id):
    user_id = get_jwt_identity()
    result = db_instance.get_collection('meal_logs').delete_one({
        "_id": ObjectId(meal_id),
        "user_id": user_id
    })
    
    if result.deleted_count > 0:
        return jsonify({"msg": "Meal deleted"}), 200
    return jsonify({"error": "Meal not found or unauthorized"}), 404

@tracker_bp.route('/day', methods=['GET'])
@jwt_required()
def get_daily_summary():
    user_id = get_jwt_identity()
    today = datetime.now().strftime("%Y-%m-%d")
    
    logs = list(db_instance.get_collection('meal_logs').find(
        {"user_id": user_id, "date": today}
    ))
    
    # Calculate Custom Targets
    target_cals, target_protein, target_carbs, target_fats = 2000, 120, 250, 70
    
    try:
        profile = db_instance.get_collection('health_profiles').find_one({"user_id": ObjectId(user_id)})
        if profile:
            weight = float(profile.get("weight_kg", 70))
            activity = profile.get("activity_level", "moderate")
            mult = 1.2 if activity == "sedentary" else (1.75 if activity == "active" else 1.55)
            
            target_cals = int(weight * 24 * mult)
            target_protein = int(weight * (1.6 if activity != "sedentary" else 1.2))
            target_fats = int((target_cals * 0.3) / 9)
            target_carbs = int((target_cals - (target_protein * 4) - (target_fats * 9)) / 4)
    except Exception as e:
        pass

    summary = {
        "calories": sum(l.get('calories', 0) for l in logs),
        "protein": sum(l.get('protein', 0) for l in logs),
        "carbs": sum(l.get('carbs', 0) for l in logs),
        "fats": sum(l.get('fats', 0) for l in logs),
        "targets": {
            "calories": target_cals,
            "protein": target_protein,
            "carbs": target_carbs,
            "fats": target_fats
        },
        "meals": [{
            "id": str(l['_id']),
            "name": l.get('name', 'Unknown'),
            "calories": l.get('calories', 0),
            "protein": l.get('protein', 0),
            "carbs": l.get('carbs', 0),
            "fats": l.get('fats', 0),
            "meal_type": l.get('meal_type', 'Snacks')
        } for l in logs]
    }
    
    return jsonify(summary), 200
