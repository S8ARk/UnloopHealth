import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app(test_config=None):
    # Initialize the Flask application
    app = Flask(__name__)

    # Default configuration
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev_secret'),
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY', 'jwt_dev_secret'),
        MONGO_URI=os.getenv('MONGO_URI', 'mongodb://localhost:27017/nutricore')
    )

    if test_config:
        app.config.from_mapping(test_config)

    # Enable CORS
    CORS(app)

    # Initialize JWT Manager
    jwt = JWTManager(app)

    # Health check route
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "healthy",
            "message": "NutriCore 2.0 API is running",
            "version": "1.0.0"
        }), 200

    # Register blueprints
    from blueprints.auth_bp import auth_bp
    from blueprints.analytics_bp import analytics_bp
    from blueprints.tracker_bp import tracker_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(tracker_bp, url_prefix='/api/tracker')

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
