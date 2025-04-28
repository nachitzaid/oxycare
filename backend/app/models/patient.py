from app import db
from datetime import datetime

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    sexe = db.Column(db.String(10), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    ville = db.Column(db.String(100), nullable=False)
    code_postal = db.Column(db.String(20), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    
    # Informations médicales
    numero_securite_sociale = db.Column(db.String(30), unique=True)
    groupe_sanguin = db.Column(db.String(10))
    allergies = db.Column(db.Text)
    antecedents = db.Column(db.Text)
    
    # Médecin traitant
    medecin_traitant = db.Column(db.String(100))
    medecin_telephone = db.Column(db.String(20))
    
    # Contact d'urgence
    contact_urgence_nom = db.Column(db.String(100))
    contact_urgence_telephone = db.Column(db.String(20))
    contact_urgence_relation = db.Column(db.String(50))
    
    # Suivi des constantes
    poids = db.Column(db.Float)
    taille = db.Column(db.Float)
    tension_arterielle = db.Column(db.String(20))
    niveau_oxygene = db.Column(db.Float)
    
    # État du dossier
    actif = db.Column(db.Boolean, default=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    equipements = db.relationship('Equipment', back_populates='patient')
    interventions = db.relationship('Intervention', back_populates='patient')
    assurances = db.relationship('PatientInsurance', back_populates='patient', cascade='all, delete-orphan')
    dossiers_medicaux = db.relationship('MedicalRecord', back_populates='patient')
    factures = db.relationship('Invoice', back_populates='patient')
    locations = db.relationship('EquipmentRental', back_populates='patient')
    
    def __repr__(self):
        return f'<Patient {self.nom} {self.prenom}>'