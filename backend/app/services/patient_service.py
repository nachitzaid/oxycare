from app.models.patient import Patient
from app.models.medical_record import MedicalRecord
from app.models.insurance import PatientInsurance
from app import db
from sqlalchemy import or_

class PatientService:
    @staticmethod
    def create_patient(patient_data):
        """
        Crée un nouveau patient
        """
        # Vérifier si le patient existe déjà (par numéro de sécurité sociale)
        if patient_data.get('numero_securite_sociale'):
            existing = Patient.query.filter_by(
                numero_securite_sociale=patient_data['numero_securite_sociale']
            ).first()
            if existing:
                raise ValueError("Un patient avec ce numéro de sécurité sociale existe déjà")
        
        # Créer le patient
        patient = Patient(**patient_data)
        db.session.add(patient)
        db.session.commit()
        
        return patient
    
    @staticmethod
    def update_patient(patient_id, patient_data):
        """
        Met à jour les informations d'un patient
        """
        patient = Patient.query.get(patient_id)
        if not patient:
            raise ValueError("Patient non trouvé")
        
        # Vérifier si le numéro de sécurité sociale est unique
        if patient_data.get('numero_securite_sociale'):
            existing = Patient.query.filter(
                Patient.numero_securite_sociale == patient_data['numero_securite_sociale'],
                Patient.id != patient_id
            ).first()
            if existing:
                raise ValueError("Un patient avec ce numéro de sécurité sociale existe déjà")
        
        # Mettre à jour le patient
        for key, value in patient_data.items():
            setattr(patient, key, value)
        
        db.session.commit()
        
        return patient
    
    @staticmethod
    def search_patients(search_term, active_only=True):
        """
        Recherche des patients par nom, prénom, numéro de sécurité sociale
        """
        query = Patient.query
        
        if active_only:
            query = query.filter(Patient.actif == True)
        
        if search_term:
            search_term = f"%{search_term}%"
            query = query.filter(
                or_(
                    Patient.nom.ilike(search_term),
                    Patient.prenom.ilike(search_term),
                    Patient.numero_securite_sociale.ilike(search_term),
                    Patient.telephone.ilike(search_term),
                    Patient.email.ilike(search_term)
                )
            )
        
        return query.order_by(Patient.nom, Patient.prenom).all()
    
    @staticmethod
    def get_patient_medical_records(patient_id):
        """
        Récupère les dossiers médicaux d'un patient
        """
        patient = Patient.query.get(patient_id)
        if not patient:
            raise ValueError("Patient non trouvé")
        
        return MedicalRecord.query.filter_by(
            patient_id=patient_id, 
            actif=True
        ).order_by(MedicalRecord.date_creation.desc()).all()
    
    @staticmethod
    def get_patient_insurances(patient_id):
        """
        Récupère les assurances d'un patient
        """
        patient = Patient.query.get(patient_id)
        if not patient:
            raise ValueError("Patient non trouvé")
        
        return PatientInsurance.query.filter_by(
            patient_id=patient_id, 
            actif=True
        ).all()
