from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.models.equipment import Equipment
from app.schemas.equipment_schema import equipment_schema, equipments_schema
from app import db

equipment_bp = Blueprint('equipments', __name__)

@equipment_bp.route('', methods=['GET'])
@jwt_required()
def get_equipments():
    """Get all equipments with filtering options"""
    # Extraction des paramètres de requête pour le filtrage
    type_equipement = request.args.get('type')
    statut = request.args.get('statut')
    patient_id = request.args.get('patient_id')
    
    # Requête de base
    query = Equipment.query
    
    # Application des filtres
    if type_equipement:
        query = query.filter(Equipment.type_equipement == type_equipement)
    if statut:
        query = query.filter(Equipment.statut == statut)
    if patient_id:
        query = query.filter(Equipment.patient_id == patient_id)
    
    # Ordonnancement
    query = query.order_by(Equipment.type_equipement, Equipment.numero_serie)
    
    # Exécution de la requête
    equipments = query.all()
    
    return jsonify(equipments_schema.dump(equipments)), 200

@equipment_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_equipment(id):
    """Get a specific equipment by ID"""
    equipment = Equipment.query.get(id)
    
    if not equipment:
        return jsonify({"error": "Equipment not found"}), 404
    
    return jsonify(equipment_schema.dump(equipment)), 200

@equipment_bp.route('', methods=['POST'])
@jwt_required()
def create_equipment():
    """Create a new equipment"""
    try:
        # Extraction et validation des données
        equipment_data = request.get_json()
        if not equipment_data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Validation via Marshmallow
        equipment_data = equipment_schema.load(equipment_data)
        
        # Création de l'équipement
        equipment = Equipment(**equipment_data)
        db.session.add(equipment)
        db.session.commit()
        
        return jsonify(equipment_schema.dump(equipment)), 201
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@equipment_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_equipment(id):
    """Update an equipment"""
    try:
        # Vérification si l'équipement existe
        equipment = Equipment.query.get(id)
        if not equipment:
            return jsonify({"error": "Equipment not found"}), 404
        
        # Extraction et validation des données
        equipment_data = request.get_json()
        if not equipment_data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Validation via Marshmallow
        equipment_data = equipment_schema.load(equipment_data, partial=True)
        
        # Mise à jour des champs de l'équipement
        for key, value in equipment_data.items():
            setattr(equipment, key, value)
        
        db.session.commit()
        
        return jsonify(equipment_schema.dump(equipment)), 200
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@equipment_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_equipment(id):
    """Delete an equipment (change status to 'réformé')"""
    try:
        # Vérification si l'équipement existe
        equipment = Equipment.query.get(id)
        if not equipment:
            return jsonify({"error": "Equipment not found"}), 404
        
        # Mise à jour du statut
        equipment.statut = 'réformé'
        db.session.commit()
        
        return jsonify({"message": "Equipment marked as 'réformé'"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
