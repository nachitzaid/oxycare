from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.models.intervention import Intervention
from app.models.service import ServiceIntervention
from app.schemas.intervention_schema import intervention_schema, interventions_schema
from app.schemas.service_schema import service_intervention_schema, service_interventions_schema
from app import db
from datetime import datetime

intervention_bp = Blueprint('interventions', __name__)

@intervention_bp.route('', methods=['GET'])
@jwt_required()
def get_interventions():
    """Get all interventions with filtering options"""
    # Extraction des paramètres de requête pour le filtrage
    type_intervention = request.args.get('type')
    statut = request.args.get('statut')
    patient_id = request.args.get('patient_id')
    equipement_id = request.args.get('equipement_id')
    technicien_id = request.args.get('technicien_id')
    date_debut = request.args.get('date_debut')
    date_fin = request.args.get('date_fin')
    
    # Requête de base
    query = Intervention.query
    
    # Application des filtres
    if type_intervention:
        query = query.filter(Intervention.type_intervention == type_intervention)
    if statut:
        query = query.filter(Intervention.statut == statut)
    if patient_id:
        query = query.filter(Intervention.patient_id == patient_id)
    if equipement_id:
        query = query.filter(Intervention.equipement_id == equipement_id)
    if technicien_id:
        query = query.filter(Intervention.technicien_id == technicien_id)
    if date_debut and date_fin:
        try:
            date_debut = datetime.strptime(date_debut, '%Y-%m-%d')
            date_fin = datetime.strptime(date_fin, '%Y-%m-%d')
            query = query.filter(Intervention.date_planifiee.between(date_debut, date_fin))
        except ValueError:
            pass  # Ignorer les filtres de date si le format est incorrect
    
    # Ordonnancement
    query = query.order_by(Intervention.date_planifiee)
    
    # Exécution de la requête
    interventions = query.all()
    
    return jsonify(interventions_schema.dump(interventions)), 200

@intervention_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_intervention(id):
    """Get a specific intervention by ID"""
    intervention = Intervention.query.get(id)
    
    if not intervention:
        return jsonify({"error": "Intervention not found"}), 404
    
    return jsonify(intervention_schema.dump(intervention)), 200

@intervention_bp.route('', methods=['POST'])
@jwt_required()
def create_intervention():
    """Create a new intervention"""
    try:
        # Extraction et validation des données
        intervention_data = request.get_json()
        if not intervention_data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Extraction des services associés (s'il y en a)
        services_data = intervention_data.pop('services', [])
        
        # Validation via Marshmallow
        intervention_data = intervention_schema.load(intervention_data)
        
        # Création de l'intervention
        intervention = Intervention(**intervention_data)
        db.session.add(intervention)
        db.session.flush()  # Pour obtenir l'ID de l'intervention
        
        # Ajout des services associés
        for service_data in services_data:
            service_data['intervention_id'] = intervention.id
            service_intervention = ServiceIntervention(**service_data)
            db.session.add(service_intervention)
        
        db.session.commit()
        
        return jsonify(intervention_schema.dump(intervention)), 201
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@intervention_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_intervention(id):
    """Update an intervention"""
    try:
        # Vérification si l'intervention existe
        intervention = Intervention.query.get(id)
        if not intervention:
            return jsonify({"error": "Intervention not found"}), 404
        
        # Extraction et validation des données
        intervention_data = request.get_json()
        if not intervention_data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Extraction des services associés (s'il y en a)
        services_data = intervention_data.pop('services', None)
        
        # Validation via Marshmallow
        intervention_data = intervention_schema.load(intervention_data, partial=True)
        
        # Mise à jour des champs de l'intervention
        for key, value in intervention_data.items():
            setattr(intervention, key, value)
        
        # Gestion des services associés si fournis
        if services_data is not None:
            # Supprimer les services existants
            ServiceIntervention.query.filter_by(intervention_id=intervention.id).delete()
            
            # Ajouter les nouveaux services
            for service_data in services_data:
                service_data['intervention_id'] = intervention.id
                service_intervention = ServiceIntervention(**service_data)
                db.session.add(service_intervention)
        
        db.session.commit()
        
        return jsonify(intervention_schema.dump(intervention)), 200
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@intervention_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_intervention(id):
    """Delete an intervention (change status to 'annulée')"""
    try:
        # Vérification si l'intervention existe
        intervention = Intervention.query.get(id)
        if not intervention:
            return jsonify({"error": "Intervention not found"}), 404
        
        # Mise à jour du statut
        intervention.statut = 'annulée'
        db.session.commit()
        
        return jsonify({"message": "Intervention marked as 'annulée'"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

