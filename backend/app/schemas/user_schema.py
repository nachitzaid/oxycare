from marshmallow import Schema, fields, validates, ValidationError, post_load
from app.models.user import User

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    nom = fields.Str(required=True)
    prenom = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)
    role = fields.Str(required=True)
    is_active = fields.Bool(dump_only=True)
    date_creation = fields.DateTime(dump_only=True)
    date_modification = fields.DateTime(dump_only=True)
    
    @validates('email')
    def validate_email(self, email):
        if User.query.filter_by(email=email).first():
            raise ValidationError('Email already exists')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

