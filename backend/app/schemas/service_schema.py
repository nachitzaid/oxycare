from marshmallow import Schema, fields, validates, ValidationError
from app.models.service import Service, ServiceIntervention

class ServiceSchema(Schema):
    id = fields.Int(dump_only=True)
    nom = fields.Str(required=True)
    type = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    
    prix_unitaire = fields.Float(allow_none=True)
    unite = fields.Str(allow_none=True)
    duree_standard = fields.Int(allow_none=True)
    
    facturable = fields.Bool()
    code_facturation = fields.Str(allow_none=True)
    
    actif = fields.Bool(dump_only=True)
    date_creation = fields.DateTime(dump_only=True)
    date_modification = fields.DateTime(dump_only=True)

service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)


class ServiceInterventionSchema(Schema):
    id = fields.Int(dump_only=True)
    intervention_id = fields.Int(required=True)
    service_id = fields.Int(required=True)
    
    quantite = fields.Float()
    duree_reelle = fields.Int(allow_none=True)
    notes = fields.Str(allow_none=True)
    
    prix_applique = fields.Float(allow_none=True)
    facturable = fields.Bool()
    
    # Relations imbriquées (optionnelles)
    service = fields.Nested('ServiceSchema', only=('id', 'nom', 'type', 'prix_unitaire'), dump_only=True)

service_intervention_schema = ServiceInterventionSchema()
service_interventions_schema = ServiceInterventionSchema(many=True)


