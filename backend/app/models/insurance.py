from app import db
from datetime import datetime

class Insurance(db.Model):
    __tablename__ = 'insurances'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))  # publique, privée, mutuelle
    
    # Informations de contact
    adresse = db.Column(db.String(200))
    ville = db.Column(db.String(100))
    code_postal = db.Column(db.String(20))
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    site_web = db.Column(db.String(100))
    
    # Contact principal
    contact_nom = db.Column(db.String(100))
    contact_telephone = db.Column(db.String(20))
    contact_email = db.Column(db.String(100))
    
    # Informations de paiement
    delai_paiement = db.Column(db.Integer, default=30)  # en jours
    
    # Métadonnées
    actif = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    patients = db.relationship('PatientInsurance', back_populates='assurance')
    factures = db.relationship('Invoice', back_populates='assurance')
    
    def __repr__(self):
        return f'<Insurance {self.nom}>'


class PatientInsurance(db.Model):
    __tablename__ = 'patient_insurances'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    assurance_id = db.Column(db.Integer, db.ForeignKey('insurances.id'), nullable=False)
    
    # Informations de couverture
    numero_adherent = db.Column(db.String(100), nullable=False)
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date)
    taux_couverture = db.Column(db.Float)  # en pourcentage
    plafond_annuel = db.Column(db.Float)
    
    # Statut
    actif = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    
    # Relations
    patient = db.relationship('Patient', back_populates='assurances')
    assurance = db.relationship('Insurance', back_populates='patients')
    
    def __repr__(self):
        return f'<PatientInsurance {self.patient_id} - {self.assurance_id}>'
