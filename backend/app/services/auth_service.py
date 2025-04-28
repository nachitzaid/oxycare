from app.models.user import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

class AuthService:
    @staticmethod
    def register_user(user_data):
        """
        Enregistre un nouvel utilisateur
        """
        # Vérifier si l'email existe déjà
        if User.query.filter_by(email=user_data['email']).first():
            raise ValueError("L'email existe déjà")
        
        # Créer l'utilisateur
        user = User(
            nom=user_data['nom'],
            prenom=user_data['prenom'],
            email=user_data['email'],
            role=user_data.get('role', 'user')
        )
        user.set_password(user_data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def authenticate_user(email, password):
        """
        Authentifie un utilisateur et génère un token
        """
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            raise ValueError("Email ou mot de passe invalide")
        
        if not user.is_active:
            raise ValueError("Compte utilisateur désactivé")
        
        access_token = create_access_token(identity=user.id)
        
        return {
            "token": access_token,
            "user": user
        }
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Récupère un utilisateur par son ID
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Utilisateur non trouvé")
        
        return user
