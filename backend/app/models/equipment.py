from app import db
from datetime import datetime

class Equipment(db.Model):
    __tablename__ = 'equipments'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_serie = db.Column(db.String(50), unique=True, nullable=False)
    modele = db.Column(db.String(100), nullable=False)
    type_equipement = db.Column(db.String(50), nullable=False)  # CPAP, oxygénothérapie, etc.
    fabricant = db.Column(db.String(100), nullable=False)
    
    # État de l'équipement
    statut = db.Column(db.String(20), nullable=False)  # neuf, en service, en maintenance, réformé
    date_acquisition = db.Column(db.Date, nullable=False)
    date_derniere_maintenance = db.Column(db.Date)
    date_prochaine_maintenance = db.Column(db.Date)
    
    # Paramètres techniques
    parametres = db.Column(db.JSON)  # Stockage des paramètres spécifiques au type d'équipement
    
    # Attribution
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    date_attribution = db.Column(db.DateTime)
    date_fin_attribution = db.Column(db.DateTime)
    
    # Historique
    notes = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    patient = db.relationship('Patient', back_populates='equipements')
    interventions = db.relationship('Intervention', back_populates='equipement')
    locations = db.relationship('EquipmentRental', back_populates='equipment')
    
    def __repr__(self):
        return f'<Equipment {self.type_equipement} - {self.numero_serie}>'
    
    @property
    def est_attribue(self):
        """Vérifie si l'équipement est actuellement attribué à un patient"""
        return self.patient_id is not None and self.date_fin_attribution is None or \
               (self.date_fin_attribution and self.date_fin_attribution > datetime.utcnow())

