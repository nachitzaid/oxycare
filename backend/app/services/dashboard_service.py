from app.models.patient import Patient
from app.models.equipment import Equipment
from app.models.intervention import Intervention
from app.models.invoice import Invoice
from app.models.medical_record import MedicalRecord
from app.models.equipment_rental import EquipmentRental
from sqlalchemy import func, and_, or_
from app import db
from datetime import datetime, timedelta

class DashboardService:
    @staticmethod
    def get_stats_summary():
        """
        Récupère un résumé des statistiques pour le tableau de bord
        """
        today = datetime.now().date()
        
        # Statistiques générales
        patients_count = Patient.query.filter_by(actif=True).count()
        equipments_count = Equipment.query.count()
        
        # Équipements par statut
        equipment_by_status = db.session.query(
            Equipment.statut, func.count(Equipment.id)
        ).group_by(Equipment.statut).all()
        equipment_status_stats = {status: count for status, count in equipment_by_status}
        
        # Interventions à venir
        next_week = today + timedelta(days=7)
        upcoming_interventions = Intervention.query.filter(
            Intervention.date_planifiee >= today,
            Intervention.date_planifiee <= next_week,
            Intervention.statut == 'planifiée'
        ).count()
        
        # Interventions par statut
        intervention_by_status = db.session.query(
            Intervention.statut, func.count(Intervention.id)
        ).group_by(Intervention.statut).all()
        intervention_status_stats = {status: count for status, count in intervention_by_status}
        
        # Factures impayées
        unpaid_invoices = Invoice.query.filter(
            Invoice.statut == 'en attente',
            Invoice.date_echeance < today
        ).count()
        
        # Équipements en retard pour la maintenance
        maintenance_due = Equipment.query.filter(
            Equipment.date_prochaine_maintenance < today,
            Equipment.statut != 'réformé'
        ).count()
        
        # Locations actives
        active_rentals = EquipmentRental.query.filter(
            EquipmentRental.date_fin == None,
            EquipmentRental.actif == True
        ).count()
        
        # Assemblage des statistiques
        return {
            "patients_count": patients_count,
            "equipments_count": equipments_count,
            "equipment_status": equipment_status_stats,
            "upcoming_interventions": upcoming_interventions,
            "intervention_status": intervention_status_stats,
            "unpaid_invoices": unpaid_invoices,
            "maintenance_due": maintenance_due,
            "active_rentals": active_rentals
        }
    
    @staticmethod
    def get_revenue_stats(period='month'):
        """
        Récupère les statistiques de chiffre d'affaires
        """
        today = datetime.now().date()
        
        if period == 'month':
            # Calculer le début du mois courant
            start_date = datetime(today.year, today.month, 1).date()
            # Calculer le début du mois suivant
            if today.month == 12:
                end_date = datetime(today.year + 1, 1, 1).date()
            else:
                end_date = datetime(today.year, today.month + 1, 1).date()
        elif period == 'year':
            # Calculer le début de l'année courante
            start_date = datetime(today.year, 1, 1).date()
            # Calculer le début de l'année suivante
            end_date = datetime(today.year + 1, 1, 1).date()
        else:
            # Par défaut, les 30 derniers jours
            start_date = today - timedelta(days=30)
            end_date = today + timedelta(days=1)
        
        # Récupérer le chiffre d'affaires total
        total_revenue = db.session.query(func.sum(Invoice.montant_ttc)).filter(
            Invoice.date_emission >= start_date,
            Invoice.date_emission < end_date,
            Invoice.statut == 'payée'
        ).scalar() or 0
        
        # Chiffre d'affaires par jour
        daily_revenue = db.session.query(
            func.date(Invoice.date_emission).label('day'),
            func.sum(Invoice.montant_ttc).label('revenue')
        ).filter(
            Invoice.date_emission >= start_date,
            Invoice.date_emission < end_date,
            Invoice.statut == 'payée'
        ).group_by('day').all()
        
        # Formater les résultats
        daily_data = {day.strftime('%Y-%m-%d'): float(revenue) for day, revenue in daily_revenue}
        
        return {
            "total_revenue": float(total_revenue),
            "period": period,
            "start_date": start_date.strftime('%Y-%m-%d'),
            "end_date": (end_date - timedelta(days=1)).strftime('%Y-%m-%d'),
            "daily_data": daily_data
        }
