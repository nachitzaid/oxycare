from app.models.equipment_rental import EquipmentRental
from app.models.equipment import Equipment
from app.models.patient import Patient
from app import db
from datetime import datetime

class EquipmentRentalService:
    @staticmethod
    def create_rental(rental_data):
        """
        Crée une nouvelle location d'équipement
        """
        # Vérifier si le patient existe
        patient = Patient.query.get(rental_data.get('patient_id'))
        if not patient:
            raise ValueError("Patient non trouvé")
        
        # Vérifier si l'équipement existe et est disponible
        equipment = Equipment.query.get(rental_data.get('equipment_id'))
        if not equipment:
            raise ValueError("Équipement non trouvé")
        
        if equipment.statut != 'disponible':
            raise ValueError("Cet équipement n'est pas disponible pour la location")
        
        # Créer la location
        rental = EquipmentRental(**rental_data)
        db.session.add(rental)
        
        # Mettre à jour le statut de l'équipement
        equipment.statut = 'en location'
        
        db.session.commit()
        
        return rental
    
    @staticmethod
    def terminate_rental(rental_id, return_data):
        """
        Termine une location d'équipement
        """
        rental = EquipmentRental.query.get(rental_id)
        if not rental:
            raise ValueError("Location non trouvée")
        
        if rental.date_fin:
            raise ValueError("Cette location est déjà terminée")
        
        # Mettre à jour la location
        rental.date_fin = return_data.get('date_fin', datetime.now().date())
        rental.etat_retour = return_data.get('etat_retour')
        rental.notes_retour = return_data.get('notes_retour')
        
        # Récupérer l'équipement
        equipment = Equipment.query.get(rental.equipment_id)
        if equipment:
            equipment.statut = 'disponible'
        
        db.session.commit()
        
        return rental
    
    @staticmethod
    def get_active_rentals():
        """
        Récupère toutes les locations actives
        """
        return EquipmentRental.query.filter(
            EquipmentRental.date_fin == None,
            EquipmentRental.actif == True
        ).all()
    
    @staticmethod
    def get_patient_rentals(patient_id):
        """
        Récupère les locations d'un patient
        """
        return EquipmentRental.query.filter(
            EquipmentRental.patient_id == patient_id,
            EquipmentRental.actif == True
        ).order_by(EquipmentRental.date_debut.desc()).all()
