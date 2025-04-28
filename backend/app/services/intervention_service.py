from app.models.intervention import Intervention
from app.models.service_intervention import ServiceIntervention
from app.models.equipment import Equipment
from app import db
from datetime import datetime, timedelta
from sqlalchemy import and_, func

class InterventionService:
    @staticmethod
    def create_intervention(intervention_data, services_data=None):
        """
        Crée une nouvelle intervention avec services associés
        """
        # Créer l'intervention
        intervention = Intervention(**intervention_data)
        db.session.add(intervention)
        db.session.flush()  # Pour obtenir l'ID de l'intervention
        
        # Ajouter les services associés
        if services_data:
            for service_data in services_data:
                service_data['intervention_id'] = intervention.id
                service_intervention = ServiceIntervention(**service_data)
                db.session.add(service_intervention)
        
        db.session.commit()
        
        return intervention
    
    @staticmethod
    def update_intervention(intervention_id, intervention_data, services_data=None):
        """
        Met à jour une intervention et ses services associés
        """
        intervention = Intervention.query.get(intervention_id)
        if not intervention:
            raise ValueError("Intervention non trouvée")
        
        # Mettre à jour l'intervention
        for key, value in intervention_data.items():
            setattr(intervention, key, value)
        
        # Gérer les services associés si fournis
        if services_data is not None:
            # Supprimer les services existants
            ServiceIntervention.query.filter_by(intervention_id=intervention.id).delete()
            
            # Ajouter les nouveaux services
            for service_data in services_data:
                service_data['intervention_id'] = intervention.id
                service_intervention = ServiceIntervention(**service_data)
                db.session.add(service_intervention)
        
        db.session.commit()
        
        return intervention
    
    @staticmethod
    def complete_intervention(intervention_id, completion_data):
        """
        Marquer une intervention comme terminée
        """
        intervention = Intervention.query.get(intervention_id)
        if not intervention:
            raise ValueError("Intervention non trouvée")
        
        if intervention.statut == 'terminée':
            raise ValueError("Cette intervention est déjà terminée")
        
        # Mise à jour des champs de l'intervention
        intervention.statut = 'terminée'
        intervention.date_fin = completion_data.get('date_fin', datetime.utcnow())
        intervention.actions_effectuees = completion_data.get('actions_effectuees')
        intervention.pieces_remplacees = completion_data.get('pieces_remplacees')
        intervention.resultat = completion_data.get('resultat')
        intervention.signature_patient = completion_data.get('signature_patient')
        intervention.signature_technicien = completion_data.get('signature_technicien')
        
        # Mise à jour de l'équipement si maintenance
        if intervention.type_intervention == 'maintenance' and intervention.equipement_id:
            equipment = Equipment.query.get(intervention.equipement_id)
            if equipment:
                equipment.date_derniere_maintenance = intervention.date_fin.date()
                equipment.date_prochaine_maintenance = (
                    intervention.date_fin.date() + timedelta(days=365)
                )
        
        db.session.commit()
        
        return intervention
    
    @staticmethod
    def get_technician_schedule(technician_id, start_date, end_date):
        """
        Récupère les interventions planifiées pour un technicien sur une période
        """
        return Intervention.query.filter(
            Intervention.technicien_id == technician_id,
            Intervention.date_planifiee >= start_date,
            Intervention.date_planifiee <= end_date,
            Intervention.statut.in_(['planifiée', 'en cours'])
        ).order_by(Intervention.date_planifiee).all()
    
    @staticmethod
    def get_interventions_by_status(status):
        """
        Récupère les interventions par statut
        """
        return Intervention.query.filter(
            Intervention.statut == status
        ).order_by(Intervention.date_planifiee).all()
    
    @staticmethod
    def get_overdue_interventions():
        """
        Récupère les interventions en retard
        """
        now = datetime.utcnow()
        return Intervention.query.filter(
            Intervention.date_planifiee < now,
            Intervention.statut.in_(['planifiée'])
        ).order_by(Intervention.date_planifiee).all()
