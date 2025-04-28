from marshmallow import Schema, fields, validates, ValidationError
from app.models.intervention import Intervention

class InterventionSchema(Schema):
    id = fields.Int(dump_only=True)
    type_intervention = fields.Str(required=True)
    statut = fields.Str(required=True)
    
    date_planifiee = fields.DateTime(required=True)
    duree_estimee = fields.Int(allow_none=True)
    
    date_debut = fields.DateTime(allow_none=True)
    date_fin = fields.DateTime(allow_none=True)
    
    patient_id = fields.Int(required=True)
    equipement_id = fields.Int(allow_none=True)
    technicien_id = fields.Int(allow_none=True)
    
    description = fields.Str(required=True)
    actions_effectuees = fields.Str(allow_none=True)
    pieces_remplacees = fields.Str(allow_none=True)
    resultat = fields.Str(allow_none=True)
    
    signature_patient = fields.Raw(allow_none=True)
    signature_technicien = fields.Raw(allow_none=True)
    
    facturable = fields.Bool()
    montant = fields.Float(allow_none=True)
    facture_id = fields.Int(allow_none=True)
    
    date_creation = fields.DateTime(dump_only=True)
    date_modification = fields.DateTime(dump_only=True)
    
    # Relations imbriquées (optionnelles)
    patient = fields.Nested('PatientSchema', only=('id', 'nom', 'prenom'), dump_only=True)
    equipement = fields.Nested('EquipmentSchema', only=('id', 'numero_serie', 'type_equipement'), dump_only=True)
    technicien = fields.Nested('UserSchema', only=('id', 'nom', 'prenom'), dump_only=True)
    services = fields.Nested('ServiceInterventionSchema', many=True, dump_only=True)

intervention_schema = InterventionSchema()
interventions_schema = InterventionSchema(many=True)

