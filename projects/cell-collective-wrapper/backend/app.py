"""
Cell Collective Wrapper - Backend API
Simple Flask server that proxies Cell Collective API
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sys
import os

# Add parent directory to path to import cell_collective_api
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from cell_collective_api import CellCollectiveAPI

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)  # Enable CORS for frontend

# Initialize API
api = CellCollectiveAPI()

# Store token (will be set via /api/set-token endpoint)
current_token = None


@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/set-token', methods=['POST'])
def set_token():
    """Set the authentication token"""
    global current_token
    data = request.json
    token = data.get('token')

    if token:
        current_token = token
        api.set_token(token)
        return jsonify({"success": True, "message": "Token set successfully"})

    return jsonify({"success": False, "message": "No token provided"}), 400


@app.route('/api/models')
def get_models():
    """Get all available models"""
    try:
        # Get all model IDs
        model_ids_dict = api.get_model_ids()

        # Combine all IDs
        all_ids = []
        for id_list in model_ids_dict.values():
            if isinstance(id_list, list):
                all_ids.extend(id_list)

        # Get card data for all models
        if all_ids:
            models = api.get_model_cards(all_ids[:10])  # Limit to 10 for demo
            return jsonify({"success": True, "models": models})

        return jsonify({"success": True, "models": []})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/model/<int:model_id>')
def get_model(model_id):
    """Get detailed model data"""
    try:
        model = api.get_model_details(model_id)

        if model:
            return jsonify({"success": True, "model": model})

        return jsonify({"success": False, "error": "Model not found"}), 404

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/initialize')
def initialize():
    """Initialize and get all metadata"""
    try:
        data = api.initialize()
        return jsonify({"success": True, "data": data})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/profile')
def get_profile():
    """Get user profile"""
    try:
        profile = api.get_profile()

        if profile:
            return jsonify({"success": True, "profile": profile})

        return jsonify({"success": False, "error": "Not authenticated"}), 401

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/courses')
def get_courses():
    """Get user's courses"""
    try:
        courses = api.get_courses()
        return jsonify({"success": True, "courses": courses})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/lesson/<int:model_id>')
def get_lesson(model_id):
    """Get lesson interface data for a specific model"""
    try:
        # Get full model data
        model = api.get_model(model_id, version=1, slim=False)

        if model:
            # Extract components and relationships for display
            lesson_data = {
                "model": {
                    "id": model_id,
                    "name": model.get("name", "Unknown Model"),
                    "description": model.get("description", ""),
                    "version": model.get("version", 1)
                },
                "components": model.get("externalComponentSet", []),
                "relationships": model.get("relationshipSet", []),
                "instructions": {
                    "title": "How to use this model",
                    "steps": [
                        "1. Review the components in the graph view",
                        "2. Adjust initial states in the control panel",
                        "3. Click 'Run Simulation' to see what happens",
                        "4. Observe how components affect each other"
                    ]
                }
            }

            return jsonify({"success": True, "lesson": lesson_data})

        return jsonify({"success": False, "error": "Model not found"}), 404

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "authenticated": current_token is not None
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Cell Collective Wrapper - Backend Starting...")
    print("="*60)
    print("\nServer: http://localhost:8000")
    print("Frontend: http://localhost:8000")
    print("\nSet token via POST to /api/set-token")
    print("   Body: {\"token\": \"your_jwt_token\"}")
    print("\nEndpoints:")
    print("   GET  /api/models          - List all models")
    print("   GET  /api/model/<id>      - Get model details")
    print("   GET  /api/profile         - Get user profile")
    print("   GET  /api/courses         - Get courses")
    print("   POST /api/set-token       - Set auth token")
    print("\n" + "="*60 + "\n")

    app.run(host='0.0.0.0', port=8000, debug=True)
