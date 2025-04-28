from app import db
from datetime import datetime

class EquipmentRental(db.Model):
    __tablename__ = 'equipment_rentals'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'), nullable=False)
    
    # Période de location
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date)  # Null si location en cours
    
    # Tarification
    tarif_journalier = db.Column(db.Float, nullable=False)
    caution = db.Column(db.Float)
    caution_versee = db.Column(db.Boolean, default=False)
    
    # État de l'équipement
    etat_depart = db.Column(db.String(50))
    notes_depart = db.Column(db.Text)
    etat_retour = db.Column(db.String(50))
    notes_retour = db.Column(db.Text)
    
    # Facturation
    mode_facturation = db.Column(db.String(20))  # journalier, mensuel, forfaitaire
    facture_id = db.Column(db.Integer, db.ForeignKey('invoices.id'))
    
    # Métadonnées
    actif = db.Column(db.Boolean, default=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    patient = db.relationship('Patient', back_populates='locations')
    equipment = db.relationship('Equipment', back_populates='locations')
    facture = db.relationship('Invoice', back_populates='locations')
    
    def __repr__(self):
        return f'<EquipmentRental {self.id} - Patient {self.patient_id} - Equipment {self.equipment_id}>'
