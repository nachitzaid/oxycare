from app import db
from datetime import datetime

class Invoice(db.Model):
    __tablename__ = 'invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_facture = db.Column(db.String(50), unique=True, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    
    # Informations de facturation
    date_emission = db.Column(db.Date, nullable=False)
    date_echeance = db.Column(db.Date, nullable=False)
    montant_ht = db.Column(db.Float, nullable=False)
    taux_tva = db.Column(db.Float, default=20.0)  # En pourcentage
    montant_ttc = db.Column(db.Float, nullable=False)
    
    # Période de facturation
    periode_debut = db.Column(db.Date, nullable=False)
    periode_fin = db.Column(db.Date, nullable=False)
    
    # Statut de paiement
    statut = db.Column(db.String(20), nullable=False)  # en attente, payée, annulée, etc.
    date_paiement = db.Column(db.Date)
    methode_paiement = db.Column(db.String(50))
    reference_paiement = db.Column(db.String(100))
    
    # Assurance et prise en charge
    assurance_id = db.Column(db.Integer, db.ForeignKey('insurances.id'))
    numero_dossier_assurance = db.Column(db.String(100))
    taux_prise_en_charge = db.Column(db.Float, default=0.0)  # En pourcentage
    montant_prise_en_charge = db.Column(db.Float, default=0.0)
    reste_a_charge = db.Column(db.Float)
    
    # Document de facture
    document_facture = db.Column(db.String(200))  # Chemin vers le fichier PDF
    
    # Métadonnées
    notes = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    patient = db.relationship('Patient', back_populates='factures')
    assurance = db.relationship('Insurance', back_populates='factures')
    items = db.relationship('InvoiceItem', back_populates='facture', cascade='all, delete-orphan')
    locations = db.relationship('EquipmentRental', back_populates='facture')
    
    def __repr__(self):
        return f'<Invoice {self.numero_facture}>'
    
    @property
    def est_payee(self):
        return self.statut == 'payée'
    
    @property
    def est_en_retard(self):
        return self.statut == 'en attente' and datetime.now().date() > self.date_echeance


class InvoiceItem(db.Model):
    __tablename__ = 'invoice_items'
    
    id = db.Column(db.Integer, primary_key=True)
    facture_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    
    # Description de la ligne
    description = db.Column(db.String(200), nullable=False)
    quantite = db.Column(db.Float, nullable=False, default=1.0)
    prix_unitaire = db.Column(db.Float, nullable=False)
    montant_total = db.Column(db.Float, nullable=False)
    
    # Références
    equipement_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    intervention_id = db.Column(db.Integer, db.ForeignKey('interventions.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    
    # Relations
    facture = db.relationship('Invoice', back_populates='items')
    equipement = db.relationship('Equipment', backref='items_facture')
    intervention = db.relationship('Intervention', backref='items_facture')
    service = db.relationship('Service')
    
    def __repr__(self):
        return f'<InvoiceItem {self.description}>'

