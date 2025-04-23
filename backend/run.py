import os
from dotenv import load_dotenv
from app import create_app, db
from app.models.user import User

load_dotenv()

app = create_app(os.getenv('FLASK_ENV', 'default'))

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)