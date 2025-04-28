from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app.schemas.user_schema import user_schema
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        user_data = request.get_json()
        
        # Validation de base
        if not user_data or not user_data.get('email') or not user_data.get('password'):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Vérifier si l'email existe déjà
        if User.query.filter_by(email=user_data.get('email')).first():
            return jsonify({"error": "Email already exists"}), 400
        
        # Créer l'utilisateur
        user = User(
            nom=user_data.get('nom'),
            prenom=user_data.get('prenom'),
            email=user_data.get('email'),
            role=user_data.get('role', 'user')
        )
        user.set_password(user_data.get('password'))
        
        db.session.add(user)
        db.session.commit()
        
        return user_schema.dump(user), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login and get access token"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing email or password"}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid email or password"}), 401
    
    if not user.is_active:
        return jsonify({"error": "User account is deactivated"}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({
        "token": access_token,
        "user": user_schema.dump(user)
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_user():
    """Get current user info"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return user_schema.dump(user), 200

