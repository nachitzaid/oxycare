from app.models.equipment import Equipment
from app.models.intervention import Intervention
from app import db
from datetime import datetime, timedelta
from sqlalchemy import and_, or_

class EquipmentService:
    @staticmethod
    def create_equipment(equipment_data):
        """
        Crée un nouvel équipement
        """
        # Vérifier si l'équipement existe déjà (par numéro de série)
        if equipment_data.get('numero_serie'):
            existing = Equipment.query.filter_by(
                numero_serie=equipment_data['numero_serie']
            ).first()
            if existing:
                raise ValueError("Un équipement avec ce numéro de série existe déjà")
        
        # Créer l'équipement
        equipment = Equipment(**equipment_data)
        db.session.add(equipment)
        db.session.commit()
        
        return equipment
    
    @staticmethod
    def update_equipment(equipment_id, equipment_data):
        """
        Met à jour les informations d'un équipement
        """
        equipment = Equipment.query.get(equipment_id)
        if not equipment:
            raise ValueError("Équipement non trouvé")
        
        # Vérifier si le numéro de série est unique
        if equipment_data.get('numero_serie'):
            existing = Equipment.query.filter(
                Equipment.numero_serie == equipment_data['numero_serie'],
                Equipment.id != equipment_id
            ).first()
            if existing:
                raise ValueError("Un équipement avec ce numéro de série existe déjà")
        
        # Mettre à jour l'équipement
        for key, value in equipment_data.items():
            setattr(equipment, key, value)
        
        db.session.commit()
        
        return equipment
    
    @staticmethod
    def assign_equipment_to_patient(equipment_id, patient_id, date_attribution=None):
        """
        Attribue un équipement à un patient
        """
        equipment = Equipment.query.get(equipment_id)
        if not equipment:
            raise ValueError("Équipement non trouvé")
        
        if equipment.est_attribue and equipment.patient_id != patient_id:
            raise ValueError("Cet équipement est déjà attribué à un autre patient")
        
        # Définir la date d'attribution
        if not date_attribution:
            date_attribution = datetime.utcnow()
        
        equipment.patient_id = patient_id
        equipment.date_attribution = date_attribution
        equipment.date_fin_attribution = None
        
        # Mettre à jour le statut
        equipment.statut = 'en service'
        
        db.session.commit()
        
        return equipment
    
    @staticmethod
    def release_equipment_from_patient(equipment_id, date_fin_attribution=None):
        """
        Libère un équipement attribué à un patient
        """
        equipment = Equipment.query.get(equipment_id)
        if not equipment:
            raise ValueError("Équipement non trouvé")
        
        if not equipment.patient_id:
            raise ValueError("Cet équipement n'est pas attribué à un patient")
        
        # Définir la date de fin d'attribution
        if not date_fin_attribution:
            date_fin_attribution = datetime.utcnow()
        
        equipment.date_fin_attribution = date_fin_attribution
        
        # Mettre à jour le statut
        equipment.statut = 'disponible'
        
        db.session.commit()
        
        return equipment
    
    @staticmethod
    def search_available_equipment(type_equipement=None):
        """
        Recherche les équipements disponibles
        """
        query = Equipment.query.filter(
            Equipment.statut == 'disponible'
        )
        
        if type_equipement:
            query = query.filter(Equipment.type_equipement == type_equipement)
        
        return query.order_by(Equipment.type_equipement, Equipment.numero_serie).all()
    
    @staticmethod
    def get_maintenance_due_equipment():
        """
        Récupère les équipements dont la maintenance est due ou prochainement due
        """
        today = datetime.now().date()
        soon = today + timedelta(days=30)
        
        return Equipment.query.filter(
            or_(
                and_(
                    Equipment.date_prochaine_maintenance <= soon,
                    Equipment.statut != 'réformé'
                ),
                and_(
                    Equipment.date_derniere_maintenance <= today - timedelta(days=365),
                    Equipment.statut != 'réformé'
                )
            )
        ).order_by(Equipment.date_prochaine_maintenance).all()

