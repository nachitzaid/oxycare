from marshmallow import Schema, fields, validates, ValidationError
from app.models.medical_record import MedicalRecord

class MedicalRecordSchema(Schema):
    id = fields.Int(dump_only=True)
    patient_id = fields.Int(required=True)
    
    date_diagnostic = fields.Date(required=True)
    medecin_prescripteur = fields.Str(required=True)
    diagnostic = fields.Str(required=True)
    
    traitement_type = fields.Str(required=True)
    traitement_details = fields.Str(required=True)
    duree_traitement = fields.Int(allow_none=True)
    date_debut_traitement = fields.Date(required=True)
    date_fin_traitement = fields.Date(allow_none=True)
    
    parametres_therapeutiques = fields.Dict(allow_none=True)
    
    numero_ordonnance = fields.Str(allow_none=True)
    document_ordonnance = fields.Str(allow_none=True)
    
    frequence_suivi = fields.Str(allow_none=True)
    notes_suivi = fields.Str(allow_none=True)
    
    resultats_examens = fields.Dict(allow_none=True)
    documents_examens = fields.List(fields.Str(), allow_none=True)
    
    actif = fields.Bool(dump_only=True)
    date_creation = fields.DateTime(dump_only=True)
    date_modification = fields.DateTime(dump_only=True)
    
    # Relations imbriquées (optionnelles)
    patient = fields.Nested('PatientSchema', only=('id', 'nom', 'prenom'), dump_only=True)

medical_record_schema = MedicalRecordSchema()
medical_records_schema = MedicalRecordSchema(many=True)
