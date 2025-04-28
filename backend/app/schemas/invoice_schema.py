from marshmallow import Schema, fields, validates, ValidationError
from app.models.invoice import Invoice, InvoiceItem

class InvoiceItemSchema(Schema):
    id = fields.Int(dump_only=True)
    facture_id = fields.Int(required=True)
    
    description = fields.Str(required=True)
    quantite = fields.Float(required=True)
    prix_unitaire = fields.Float(required=True)
    montant_total = fields.Float(required=True)
    
    equipement_id = fields.Int(allow_none=True)
    intervention_id = fields.Int(allow_none=True)
    service_id = fields.Int(allow_none=True)
    
    # Relations imbriquées (optionnelles)
    equipement = fields.Nested('EquipmentSchema', only=('id', 'numero_serie', 'type_equipement'), dump_only=True)
    intervention = fields.Nested('InterventionSchema', only=('id', 'type_intervention', 'date_planifiee'), dump_only=True)
    service = fields.Nested('ServiceSchema', only=('id', 'nom', 'type'), dump_only=True)

invoice_item_schema = InvoiceItemSchema()
invoice_items_schema = InvoiceItemSchema(many=True)


class InvoiceSchema(Schema):
    id = fields.Int(dump_only=True)
    numero_facture = fields.Str(required=True)
    patient_id = fields.Int(required=True)
    
    date_emission = fields.Date(required=True)
    date_echeance = fields.Date(required=True)
    montant_ht = fields.Float(required=True)
    taux_tva = fields.Float()
    montant_ttc = fields.Float(required=True)
    
    periode_debut = fields.Date(required=True)
    periode_fin = fields.Date(required=True)
    
    statut = fields.Str(required=True)
    date_paiement = fields.Date(allow_none=True)
    methode_paiement = fields.Str(allow_none=True)
    reference_paiement = fields.Str(allow_none=True)
    
    assurance_id = fields.Int(allow_none=True)
    numero_dossier_assurance = fields.Str(allow_none=True)
    taux_prise_en_charge = fields.Float(allow_none=True)
    montant_prise_en_charge = fields.Float(allow_none=True)
    reste_a_charge = fields.Float(allow_none=True)
    
    document_facture = fields.Str(allow_none=True)
    
    notes = fields.Str(allow_none=True)
    date_creation = fields.DateTime(dump_only=True)
    date_modification = fields.DateTime(dump_only=True)
    
    # Relations imbriquées
    patient = fields.Nested('PatientSchema', only=('id', 'nom', 'prenom'), dump_only=True)
    assurance = fields.Nested('InsuranceSchema', only=('id', 'nom'), dump_only=True)
    items = fields.Nested('InvoiceItemSchema', many=True, dump_only=True)
    
    @validates('numero_facture')
    def validate_numero_facture(self, numero_facture):
        invoice = Invoice.query.filter_by(numero_facture=numero_facture).first()
        if invoice:
            raise ValidationError('Ce numéro de facture existe déjà')

invoice_schema = InvoiceSchema()
invoices_schema = InvoiceSchema(many=True)
