from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.ml_service import ml_service
from models.database import db_instance
from datetime import datetime

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/profile', methods=['POST'])
@jwt_required()
def save_profile():
    """ Save detailed health profile questionnaire results """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Required fields validation
    required = ['age', 'height_cm', 'weight_kg', 'gender']
    if not all(k in data for k in required):
        return jsonify({"msg": "Missing required health metrics"}), 400
        
    # Calculate BMI
    bmi = float(data['weight_kg']) / (float(data['height_cm']) / 100)**2
    data['bmi'] = round(bmi, 2)
    
    db_instance.update_user_profile(user_id, data)
    return jsonify({"msg": "Profile updated successfully", "bmi": data['bmi']}), 200

@analytics_bp.route('/predict', methods=['GET'])
@jwt_required()
def get_predictions():
    """ Get ML-powered risk assessments based on profile and logs """
    user_id = get_jwt_identity()
    user = db_instance.get_user_profile(user_id)
    
    if not user or 'profile' not in user:
        return jsonify({"msg": "Please complete your health profile first"}), 404
        
    profile = user['profile']
    
    # Enrich profile with recent logs if available (fallback to profile defaults)
    # In a real app, we'd fetch the last 7 days of activity_logs here.
    
    prediction = ml_service.predict_risk(profile)
    
    return jsonify({
        "status": "success",
        "data": prediction,
        "user_name": user.get('full_name', 'User')
    }), 200

@analytics_bp.route('/log', methods=['POST'])
@jwt_required()
def log_activity():
    """ Log daily stats: water, sleep, exercise """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    today = datetime.now().strftime("%Y-%m-%d")
    data['date'] = today
    
    db_instance.log_activity(user_id, data)
    return jsonify({"msg": "Activity logged successfully"}), 200
