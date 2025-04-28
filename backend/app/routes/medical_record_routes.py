from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from app.models.medical_record import MedicalRecord
from app.schemas.medical_record_schema import medical_record_schema, medical_records_schema
from app import db

medical_record_bp = Blueprint('medical_records', __name__)

@medical_record_bp.route('', methods=['GET'])
@jwt_required()
def get_medical_records():
    """Get all medical records with filtering options"""
    # Extraction des paramètres de requête pour le filtrage
    patient_id = request.args.get('patient_id')
    actif = request.args.get('actif')
    
    # Requête de base
    query = MedicalRecord.query
    
    # Application des filtres
    if patient_id:
        query = query.filter(MedicalRecord.patient_id == patient_id)
    if actif is not None:
        actif_bool = actif.lower() == 'true'
        query = query.filter(MedicalRecord.actif == actif_bool)
    
    # Ordonnancement
    query = query.order_by(MedicalRecord.date_creation.desc())
    
    # Exécution de la requête
    records = query.all()
    
    return jsonify(medical_records_schema.dump(records)), 200

@medical_record_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_medical_record(id):
    """Get a specific medical record by ID"""
    record = MedicalRecord.query.get(id)
    
    if not record:
        return jsonify({"error": "Medical record not found"}), 404
    
    return jsonify(medical_record_schema.dump(record)), 200

@medical_record_bp.route('', methods=['POST'])
@jwt_required()
def create_medical_record():
    """Create a new medical record"""
    try:
        # Extraction et validation des données
        record_data = request.get_json()
        if not record_data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Validation via Marshmallow
        record_data = medical_record_schema.load(record_data)
        
        # Création du dossier médical
        record = MedicalRecord(**record_data)
        db.session.add(record)
        db.session.commit()
        
        return jsonify(medical_record_schema.dump(record)), 201
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@medical_record_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_medical_record(id):
    """Update a medical record"""
    try:
        # Vérification si le dossier existe
        record = MedicalRecord.query.get(id)
        if not record:
            return jsonify({"error": "Medical record not found"}), 404
        
        # Extraction et validation des données
        record_data = request.get_json()
        if not record_data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Validation via Marshmallow
        record_data = medical_record_schema.load(record_data, partial=True)
        
        # Mise à jour des champs du dossier
        for key, value in record_data.items():
            setattr(record, key, value)
        
        db.session.commit()
        
        return jsonify(medical_record_schema.dump(record)), 200
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@medical_record_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_medical_record(id):
    """Delete a medical record (soft delete)"""
    try:
        # Vérification si le dossier existe
        record = MedicalRecord.query.get(id)
        if not record:
            return jsonify({"error": "Medical record not found"}), 404
        
        # Soft delete
        record.actif = False
        db.session.commit()
        
        return jsonify({"message": "Medical record successfully deactivated"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

