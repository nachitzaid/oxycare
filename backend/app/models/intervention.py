from app import db
from datetime import datetime

class Intervention(db.Model):
    __tablename__ = 'interventions'
    
    id = db.Column(db.Integer, primary_key=True)
    type_intervention = db.Column(db.String(50), nullable=False)  # installation, maintenance, réparation, etc.
    statut = db.Column(db.String(20), nullable=False)  # planifiée, en cours, terminée, annulée
    
    # Planification
    date_planifiee = db.Column(db.DateTime, nullable=False)
    duree_estimee = db.Column(db.Integer)  # en minutes
    
    # Exécution
    date_debut = db.Column(db.DateTime)
    date_fin = db.Column(db.DateTime)
    
    # Associations
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    equipement_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    technicien_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Détails de l'intervention
    description = db.Column(db.Text, nullable=False)
    actions_effectuees = db.Column(db.Text)
    pieces_remplacees = db.Column(db.Text)
    resultat = db.Column(db.Text)
    
    # Signature
    signature_patient = db.Column(db.LargeBinary)
    signature_technicien = db.Column(db.LargeBinary)
    
    # Facturation
    facturable = db.Column(db.Boolean, default=True)
    montant = db.Column(db.Float)
    facture_id = db.Column(db.Integer)  # Lien vers une future table de factures
    
    # Métadonnées
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    patient = db.relationship('Patient', back_populates='interventions')
    equipement = db.relationship('Equipment', back_populates='interventions')
    technicien = db.relationship('User', backref='interventions')
    services = db.relationship('ServiceIntervention', back_populates='intervention', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Intervention {self.type_intervention} - {self.date_planifiee}>'
