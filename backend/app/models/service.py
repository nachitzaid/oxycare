from app import db
from datetime import datetime

class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Installation, Formation, Entretien, Vente, etc.
    description = db.Column(db.Text)
    
    # Tarification
    prix_unitaire = db.Column(db.Float)
    unite = db.Column(db.String(20))  # heure, forfait, session, etc.
    duree_standard = db.Column(db.Integer)  # en minutes
    
    # Options de facturation
    facturable = db.Column(db.Boolean, default=True)
    code_facturation = db.Column(db.String(20))  # Pour les systèmes de remboursement
    
    # Métadonnées
    actif = db.Column(db.Boolean, default=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    interventions = db.relationship('ServiceIntervention', back_populates='service')
    items_facture = db.relationship('InvoiceItem', back_populates='service')
    def __repr__(self):
        return f'<Service {self.nom} ({self.type})>'


class ServiceIntervention(db.Model):
    __tablename__ = 'service_interventions'
    
    id = db.Column(db.Integer, primary_key=True)
    intervention_id = db.Column(db.Integer, db.ForeignKey('interventions.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    
    # Détails de l'exécution
    quantite = db.Column(db.Float, default=1.0)
    duree_reelle = db.Column(db.Integer)  # en minutes
    notes = db.Column(db.Text)
    
    # Facturation
    prix_applique = db.Column(db.Float)  # Prix qui peut différer du prix standard
    facturable = db.Column(db.Boolean, default=True)
    
    # Relations
    intervention = db.relationship('Intervention', back_populates='services')
    service = db.relationship('Service', back_populates='interventions')
    
    def __repr__(self):
        return f'<ServiceIntervention {self.service_id} - {self.intervention_id}>'

