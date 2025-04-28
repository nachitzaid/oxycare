from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from app.models.equipment_rental import EquipmentRental
from app.schemas.equipment_rental_schema import equipment_rental_schema, equipment_rentals_schema
from app import db

rental_bp = Blueprint('rentals', __name__)

@rental_bp.route('', methods=['GET'])
@jwt_required()
def get_rentals():
    """Get all equipment rentals with filtering options"""
    # Extraction des paramètres de requête pour le filtrage
    patient_id = request.args.get('patient_id')
    equipment_id = request.args.get('equipment_id')
    actif = request.args.get('actif')
    
    # Requête de base
    query = EquipmentRental.query
    
    # Application des filtres
    if patient_id:
        query = query.filter(EquipmentRental.patient_id == patient_id)
    if equipment_id:
        query = query.filter(EquipmentRental.equipment_id == equipment_id)
    if actif is not None:
        actif_bool = actif.lower() == 'true'
        query = query.filter(EquipmentRental.actif == actif_bool)
    
    # Ordonnancement
    query = query.order_by(EquipmentRental.date_debut.desc())
    
    # Exécution de la requête
    rentals = query.all()
    
    return jsonify(equipment_rentals_schema.dump(rentals)), 200

@rental_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_rental(id):
    """Get a specific equipment rental by ID"""
    rental = EquipmentRental.query.get(id)
    
    if not rental:
        return jsonify({"error": "Equipment rental not found"}), 404
    
    return jsonify(equipment_rental_schema.dump(rental)), 200

@rental_bp.route('', methods=['POST'])
@jwt_required()
def create_rental():
    """Create a new equipment rental"""
    try:
        # Extraction et validation des données
        rental_data = request.get_json()
        if not rental_data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Validation via Marshmallow
        rental_data = equipment_rental_schema.load(rental_data)
        
        # Création de la location
        rental = EquipmentRental(**rental_data)
        db.session.add(rental)
        db.session.commit()
        
        return jsonify(equipment_rental_schema.dump(rental)), 201
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@rental_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_rental(id):
    """Update an equipment rental"""
    try:
        # Vérification si la location existe
        rental = EquipmentRental.query.get(id)
        if not rental:
            return jsonify({"error": "Equipment rental not found"}), 404
        
        # Extraction et validation des données
        rental_data = request.get_json()
        if not rental_data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Validation via Marshmallow
        rental_data = equipment_rental_schema.load(rental_data, partial=True)
        
        # Mise à jour des champs de la location
        for key, value in rental_data.items():
            setattr(rental, key, value)
        
        db.session.commit()
        
        return jsonify(equipment_rental_schema.dump(rental)), 200
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@rental_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_rental(id):
    """Delete an equipment rental (soft delete)"""
    try:
        # Vérification si la location existe
        rental = EquipmentRental.query.get(id)
        if not rental:
            return jsonify({"error": "Equipment rental not found"}), 404
        
        # Soft delete
        rental.actif = False
        db.session.commit()
        
        return jsonify({"message": "Equipment rental successfully deactivated"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400