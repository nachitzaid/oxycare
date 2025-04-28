from marshmallow import Schema, fields, validates, ValidationError
from app.models.equipment import Equipment

class EquipmentSchema(Schema):
    id = fields.Int(dump_only=True)
    numero_serie = fields.Str(required=True)
    modele = fields.Str(required=True)
    type_equipement = fields.Str(required=True)
    fabricant = fields.Str(required=True)
    
    statut = fields.Str(required=True)
    date_acquisition = fields.Date(required=True)
    date_derniere_maintenance = fields.Date(allow_none=True)
    date_prochaine_maintenance = fields.Date(allow_none=True)
    
    parametres = fields.Dict(allow_none=True)
    
    patient_id = fields.Int(allow_none=True)
    date_attribution = fields.DateTime(allow_none=True)
    date_fin_attribution = fields.DateTime(allow_none=True)
    
    notes = fields.Str(allow_none=True)
    date_creation = fields.DateTime(dump_only=True)
    date_modification = fields.DateTime(dump_only=True)
    
    # Relations imbriquées (optionnelles)
    patient = fields.Nested('PatientSchema', only=('id', 'nom', 'prenom'), dump_only=True)
    
    @validates('numero_serie')
    def validate_numero_serie(self, numero_serie):
        equipment = Equipment.query.filter_by(numero_serie=numero_serie).first()
        if equipment:
            raise ValidationError('Ce numéro de série existe déjà')

equipment_schema = EquipmentSchema()
equipments_schema = EquipmentSchema(many=True)

