from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config import config


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints
    from .routes.auth_routes import auth_bp
    from .routes.patient_routes import patient_bp
    from .routes.equipment_routes import equipment_bp
    from .routes.intervention_routes import intervention_bp
    from .routes.medical_record_routes import medical_record_bp
    from .routes.invoice_routes import invoice_bp
    from .routes.service_routes import service_bp
    from .routes.equipment_rental_routes import rental_bp
    from .routes.dashboard_routes import dashboard_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(patient_bp, url_prefix='/api/patients')
    app.register_blueprint(equipment_bp, url_prefix='/api/equipments')
    app.register_blueprint(intervention_bp, url_prefix='/api/interventions')
    app.register_blueprint(medical_record_bp, url_prefix='/api/medical-records')
    app.register_blueprint(invoice_bp, url_prefix='/api/invoices')
    app.register_blueprint(service_bp, url_prefix='/api/services')
    app.register_blueprint(rental_bp, url_prefix='/api/rentals')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy'}
    
    return app