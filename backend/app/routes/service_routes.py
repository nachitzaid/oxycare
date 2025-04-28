from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from app.models.service import Service
from app.schemas.service_schema import service_schema, services_schema
from app import db

service_bp = Blueprint('services', __name__)

@service_bp.route('', methods=['GET'])
@jwt_required()
def get_services():
    """Get all services with filtering options"""
    # Extraction des paramètres de requête pour le filtrage
    type_service = request.args.get('type')
    actif = request.args.get('actif')
    
    # Requête de base
    query = Service.query
    
    # Application des filtres
    if type_service:
        query = query.filter(Service.type == type_service)
    if actif is not None:
        actif_bool = actif.lower() == 'true'
        query = query.filter(Service.actif == actif_bool)
    
    # Ordonnancement
    query = query.order_by(Service.type, Service.nom)
    
    # Exécution de la requête
    services = query.all()
    
    return jsonify(services_schema.dump(services)), 200

@service_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_service(id):
    """Get a specific service by ID"""
    service = Service.query.get(id)
    
    if not service:
        return jsonify({"error": "Service not found"}), 404
    
    return jsonify(service_schema.dump(service)), 200

@service_bp.route('', methods=['POST'])
@jwt_required()
def create_service():
    """Create a new service"""
    try:
        # Extraction et validation des données
        service_data = request.get_json()
        if not service_data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Validation via Marshmallow
        service_data = service_schema.load(service_data)
        
        # Création du service
        service = Service(**service_data)
        db.session.add(service)
        db.session.commit()
        
        return jsonify(service_schema.dump(service)), 201
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@service_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_service(id):
    """Update a service"""
    try:
        # Vérification si le service existe
        service = Service.query.get(id)
        if not service:
            return jsonify({"error": "Service not found"}), 404
        
        # Extraction et validation des données
        service_data = request.get_json()
        if not service_data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Validation via Marshmallow
        service_data = service_schema.load(service_data, partial=True)
        
        # Mise à jour des champs du service
        for key, value in service_data.items():
            setattr(service, key, value)
        
        db.session.commit()
        
        return jsonify(service_schema.dump(service)), 200
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@service_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_service(id):
    """Delete a service (soft delete)"""
    try:
        # Vérification si le service existe
        service = Service.query.get(id)
        if not service:
            return jsonify({"error": "Service not found"}), 404
        
        # Soft delete
        service.actif = False
        db.session.commit()
        
        return jsonify({"message": "Service successfully deactivated"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400