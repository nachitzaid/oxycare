from app import db
from app.models.service import Service
from datetime import datetime

def initialize_services():
    """Initialise les services proposés par OxyLife"""
    
    services = [
        {
            'nom': 'Installation d\'équipement',
            'type': 'Installation',
            'description': 'Installation et configuration d\'équipement médical à domicile',
            'prix_unitaire': 50.00,
            'unite': 'forfait',
            'duree_standard': 60,
            'facturable': True
        },
        {
            'nom': 'Formation patient',
            'type': 'Formation',
            'description': 'Formation du patient à l\'utilisation de son équipement',
            'prix_unitaire': 40.00,
            'unite': 'session',
            'duree_standard': 45,
            'facturable': True
        },
        {
            'nom': 'Entretien préventif',
            'type': 'Entretien',
            'description': 'Maintenance préventive des équipements',
            'prix_unitaire': 35.00,
            'unite': 'forfait',
            'duree_standard': 30,
            'facturable': True
        },
        {
            'nom': 'Vente d\'équipement',
            'type': 'Vente',
            'description': 'Vente de matériel médical',
            'prix_unitaire': 0.00,  # Dépend de l'équipement
            'unite': 'unité',
            'duree_standard': 0,
            'facturable': True
        },
        {
            'nom': 'Mise à jour logicielle',
            'type': 'Mise à jour',
            'description': 'Mise à jour des logiciels des équipements',
            'prix_unitaire': 25.00,
            'unite': 'forfait',
            'duree_standard': 20,
            'facturable': True
        },
        {
            'nom': 'Réparation standard',
            'type': 'Réparation',
            'description': 'Réparation d\'équipement médical',
            'prix_unitaire': 60.00,
            'unite': 'heure',
            'duree_standard': 60,
            'facturable': True
        },
        {
            'nom': 'Location d\'équipement',
            'type': 'Location',
            'description': 'Location d\'équipement médical',
            'prix_unitaire': 0.00,  # Dépend de l'équipement et de la durée
            'unite': 'jour',
            'duree_standard': 0,
            'facturable': True
        },
        {
            'nom': 'Évaluation technique à domicile',
            'type': 'Évaluation',
            'description': 'Évaluation des besoins du patient à domicile',
            'prix_unitaire': 75.00,
            'unite': 'visite',
            'duree_standard': 90,
            'facturable': True
        }
    ]
    
    
    for service_data in services:
        # Vérifier si le service existe déjà
        existing = Service.query.filter_by(nom=service_data['nom']).first()
        if not existing:
            service = Service(**service_data)
            db.session.add(service)
    
    db.session.commit()
    print('Services initialisés avec succès')