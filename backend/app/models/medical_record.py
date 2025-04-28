from app import db
from datetime import datetime

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    
    # Diagnostic et prescription
    date_diagnostic = db.Column(db.Date, nullable=False)
    medecin_prescripteur = db.Column(db.String(100), nullable=False)
    diagnostic = db.Column(db.Text, nullable=False)
    
    # Traitement prescrit
    traitement_type = db.Column(db.String(50), nullable=False)  # CPAP, oxygénothérapie, etc.
    traitement_details = db.Column(db.Text, nullable=False)
    duree_traitement = db.Column(db.Integer)  # en jours, null si indéterminé
    date_debut_traitement = db.Column(db.Date, nullable=False)
    date_fin_traitement = db.Column(db.Date)
    
    # Paramètres thérapeutiques
    parametres_therapeutiques = db.Column(db.JSON)  # Stockage des paramètres spécifiques au traitement
    
    # Ordonnance
    numero_ordonnance = db.Column(db.String(50))
    document_ordonnance = db.Column(db.String(200))  # Chemin vers le fichier de l'ordonnance
    
    # Suivi et évaluation
    frequence_suivi = db.Column(db.String(50))  # quotidien, hebdomadaire, mensuel
    notes_suivi = db.Column(db.Text)
    
    # Résultats d'examens
    resultats_examens = db.Column(db.JSON)  # Résultats d'examens structurés
    documents_examens = db.Column(db.JSON)  # Liste des chemins vers les documents
    
    # Métadonnées
    actif = db.Column(db.Boolean, default=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    patient = db.relationship('Patient', back_populates='dossiers_medicaux')
    
    def __repr__(self):
        return f'<MedicalRecord {self.id} - Patient {self.patient_id}>'

