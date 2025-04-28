from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.models.patient import Patient
from app.schemas.patient_schema import patient_schema, patients_schema
from app import db

patient_bp = Blueprint('patients', __name__)

@patient_bp.route('', methods=['GET'])
@jwt_required()
def get_patients():
    """Get all patients with filtering options"""
    # Extraction des paramètres de requête pour le filtrage
    nom = request.args.get('nom')
    prenom = request.args.get('prenom')
    actif = request.args.get('actif')
    
    # Requête de base
    query = Patient.query
    
    # Application des filtres
    if nom:
        query = query.filter(Patient.nom.ilike(f'%{nom}%'))
    if prenom:
        query = query.filter(Patient.prenom.ilike(f'%{prenom}%'))
    if actif is not None:
        actif_bool = actif.lower() == 'true'
        query = query.filter(Patient.actif == actif_bool)
    
    # Ordonnancement
    query = query.order_by(Patient.nom, Patient.prenom)
    
    # Exécution de la requête
    patients = query.all()
    
    return jsonify(patients_schema.dump(patients)), 200

@patient_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_patient(id):
    """Get a specific patient by ID"""
    patient = Patient.query.get(id)
    
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    
    return jsonify(patient_schema.dump(patient)), 200

@patient_bp.route('', methods=['POST'])
@jwt_required()
def create_patient():
    """Create a new patient"""
    try:
        # Extraction et validation des données
        patient_data = request.get_json()
        if not patient_data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Validation via Marshmallow
        patient_data = patient_schema.load(patient_data)
        
        # Création du patient
        patient = Patient(**patient_data)
        db.session.add(patient)
        db.session.commit()
        
        return jsonify(patient_schema.dump(patient)), 201
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@patient_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_patient(id):
    """Update a patient"""
    try:
        # Vérification si le patient existe
        patient = Patient.query.get(id)
        if not patient:
            return jsonify({"error": "Patient not found"}), 404
        
        # Extraction et validation des données
        patient_data = request.get_json()
        if not patient_data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Validation via Marshmallow
        patient_data = patient_schema.load(patient_data, partial=True)
        
        # Mise à jour des champs du patient
        for key, value in patient_data.items():
            setattr(patient, key, value)
        
        db.session.commit()
        
        return jsonify(patient_schema.dump(patient)), 200
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@patient_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_patient(id):
    """Delete a patient (soft delete)"""
    try:
        # Vérification si le patient existe
        patient = Patient.query.get(id)
        if not patient:
            return jsonify({"error": "Patient not found"}), 404
        
        # Soft delete (désactivation)
        patient.actif = False
        db.session.commit()
        
        return jsonify({"message": "Patient successfully deactivated"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

