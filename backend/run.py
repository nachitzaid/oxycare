# backend/run.py
import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import User, Patient, Equipment, Intervention, MedicalRecord, Insurance, Invoice, Service, EquipmentRental

load_dotenv()

app = create_app(os.getenv('FLASK_ENV', 'default'))

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Patient': Patient, 
        'Equipment': Equipment, 
        'Intervention': Intervention,
        'MedicalRecord': MedicalRecord,
        'Insurance': Insurance,
        'Invoice': Invoice,
        'Service': Service,
        'EquipmentRental': EquipmentRental
    }

@app.cli.command('create-admin')
def create_admin():
    """Créer un utilisateur administrateur"""
    admin = User.query.filter_by(email='admin@oxycare.com').first()
    if admin:
        print('L\'utilisateur admin existe déjà')
        return
    
    admin = User(
        nom='Admin',
        prenom='OxyCare',
        email='admin@oxycare.com',
        role='admin',
        is_active=True
    )
    admin.set_password('admin')
    
    db.session.add(admin)
    db.session.commit()
    print('Utilisateur admin créé avec succès')

@app.cli.command('init-services')
def init_services():
    """Initialiser les services de OxyLife"""
    from app.utils.services_init import initialize_services
    initialize_services()
    print('Services initialisés avec succès')

@app.cli.command('init-db')
def init_db():
    """Initialiser la base de données avec les données de base"""
    # D'abord créer les tables
    db.create_all()
    
    # Créer l'admin
    admin = User.query.filter_by(email='admin@oxycare.com').first()
    if not admin:
        admin = User(
            nom='Admin',
            prenom='OxyCare',
            email='admin@oxycare.com',
            role='admin',
            is_active=True
        )
        admin.set_password('admin')
        db.session.add(admin)
    
    # Créer un utilisateur technicien
    technicien = User.query.filter_by(email='technicien@oxycare.com').first()
    if not technicien:
        technicien = User(
            nom='Technicien',
            prenom='OxyCare',
            email='technicien@oxycare.com',
            role='technicien',
            is_active=True
        )
        technicien.set_password('technicien')
        db.session.add(technicien)
    
    # Initialiser les services
    from app.utils.services_init import initialize_services
    initialize_services()
    
    db.session.commit()
    print('Base de données initialisée avec succès')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)