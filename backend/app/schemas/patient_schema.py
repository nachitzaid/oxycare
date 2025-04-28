from marshmallow import Schema, fields, validates, ValidationError
from app.models.patient import Patient

class PatientSchema(Schema):
    id = fields.Int(dump_only=True)
    nom = fields.Str(required=True)
    prenom = fields.Str(required=True)
    date_naissance = fields.Date(required=True)
    sexe = fields.Str(required=True)
    adresse = fields.Str(required=True)
    ville = fields.Str(required=True)
    code_postal = fields.Str(required=True)
    telephone = fields.Str(required=True)
    email = fields.Email(allow_none=True)
    
    numero_securite_sociale = fields.Str(allow_none=True)
    groupe_sanguin = fields.Str(allow_none=True)
    allergies = fields.Str(allow_none=True)
    antecedents = fields.Str(allow_none=True)
    
    medecin_traitant = fields.Str(allow_none=True)
    medecin_telephone = fields.Str(allow_none=True)
    
    contact_urgence_nom = fields.Str(allow_none=True)
    contact_urgence_telephone = fields.Str(allow_none=True)
    contact_urgence_relation = fields.Str(allow_none=True)
    
    poids = fields.Float(allow_none=True)
    taille = fields.Float(allow_none=True)
    tension_arterielle = fields.Str(allow_none=True)
    niveau_oxygene = fields.Float(allow_none=True)
    
    actif = fields.Bool(dump_only=True)
    date_creation = fields.DateTime(dump_only=True)
    date_modification = fields.DateTime(dump_only=True)
    
    @validates('numero_securite_sociale')
    def validate_numero_securite_sociale(self, numero_securite_sociale):
        if numero_securite_sociale:
            patient = Patient.query.filter_by(numero_securite_sociale=numero_securite_sociale).first()
            if patient:
                raise ValidationError('Ce numéro de sécurité sociale existe déjà')

patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)

