from app.models.medical_record import MedicalRecord
from app.models.patient import Patient
from app import db

class MedicalRecordService:
    @staticmethod
    def create_medical_record(record_data):
        """
        Crée un nouveau dossier médical
        """
        # Vérifier si le patient existe
        patient = Patient.query.get(record_data.get('patient_id'))
        if not patient:
            raise ValueError("Patient non trouvé")
        
        # Créer le dossier médical
        record = MedicalRecord(**record_data)
        db.session.add(record)
        db.session.commit()
        
        return record
    
    @staticmethod
    def update_medical_record(record_id, record_data):
        """
        Met à jour un dossier médical
        """
        record = MedicalRecord.query.get(record_id)
        if not record:
            raise ValueError("Dossier médical non trouvé")
        
        # Mettre à jour le dossier
        for key, value in record_data.items():
            setattr(record, key, value)
        
        db.session.commit()
        
        return record
    
    @staticmethod
    def add_exam_result(record_id, exam_data):
        """
        Ajoute un résultat d'examen à un dossier médical
        """
        record = MedicalRecord.query.get(record_id)
        if not record:
            raise ValueError("Dossier médical non trouvé")
        
        # Initialiser le dictionnaire si nécessaire
        if not record.resultats_examens:
            record.resultats_examens = {}
        
        # Ajouter ou mettre à jour le résultat d'examen
        exam_date = exam_data.pop('date', datetime.now().strftime('%Y-%m-%d'))
        
        if exam_date not in record.resultats_examens:
            record.resultats_examens[exam_date] = []
        
        record.resultats_examens[exam_date].append(exam_data)
        
        db.session.commit()
        
        return record
    
    @staticmethod
    def add_document(record_id, document_path, document_type):
        """
        Ajoute un document à un dossier médical
        """
        record = MedicalRecord.query.get(record_id)
        if not record:
            raise ValueError("Dossier médical non trouvé")
        
        # Initialiser la liste si nécessaire
        if not record.documents_examens:
            record.documents_examens = []
        
        # Ajouter le document
        document_info = {
            'path': document_path,
            'type': document_type,
            'date_ajout': datetime.now().strftime('%Y-%m-%d')
        }
        
        record.documents_examens.append(document_info)
        
        db.session.commit()
        
        return record
