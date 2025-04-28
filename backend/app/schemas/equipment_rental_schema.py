from marshmallow import Schema, fields, validates, ValidationError
from app.models.equipment_rental import EquipmentRental

class EquipmentRentalSchema(Schema):
    id = fields.Int(dump_only=True)
    patient_id = fields.Int(required=True)
    equipment_id = fields.Int(required=True)
    
    date_debut = fields.Date(required=True)
    date_fin = fields.Date(allow_none=True)
    
    tarif_journalier = fields.Float(required=True)
    caution = fields.Float(allow_none=True)
    caution_versee = fields.Bool()
    
    etat_depart = fields.Str(allow_none=True)
    notes_depart = fields.Str(allow_none=True)
    etat_retour = fields.Str(allow_none=True)
    notes_retour = fields.Str(allow_none=True)
    
    mode_facturation = fields.Str(allow_none=True)
    facture_id = fields.Int(allow_none=True)
    
    actif = fields.Bool(dump_only=True)
    date_creation = fields.DateTime(dump_only=True)
    date_modification = fields.DateTime(dump_only=True)
    
    # Relations imbriquées (optionnelles)
    patient = fields.Nested('PatientSchema', only=('id', 'nom', 'prenom'), dump_only=True)
    equipment = fields.Nested('EquipmentSchema', only=('id', 'numero_serie', 'type_equipement'), dump_only=True)
    facture = fields.Nested('InvoiceSchema', only=('id', 'numero_facture'), dump_only=True)

equipment_rental_schema = EquipmentRentalSchema()
equipment_rentals_schema = EquipmentRentalSchema(many=True)
