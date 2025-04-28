from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.models.patient import Patient
from app.models.equipment import Equipment
from app.models.intervention import Intervention
from app.models.invoice import Invoice
from sqlalchemy import func
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get statistical data for the dashboard"""
    # Statistiques de base
    total_patients = Patient.query.filter_by(actif=True).count()
    total_equipments = Equipment.query.count()
    
    # Équipements par statut
    equipment_by_status = db.session.query(
        Equipment.statut, func.count(Equipment.id)
    ).group_by(Equipment.statut).all()
    equipment_status_stats = {status: count for status, count in equipment_by_status}
    
    # Interventions à venir
    today = datetime.now().date()
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
    
    # Chiffre d'affaires du mois en cours
    current_month_start = datetime(today.year, today.month, 1).date()
    next_month_start = (current_month_start + timedelta(days=32)).replace(day=1)
    current_month_revenue = db.session.query(func.sum(Invoice.montant_ttc)).filter(
        Invoice.date_emission >= current_month_start,
        Invoice.date_emission < next_month_start,
        Invoice.statut == 'payée'
    ).scalar() or 0
    
    # Assemblage des statistiques
    stats = {
        "total_patients": total_patients,
        "total_equipments": total_equipments,
        "equipment_by_status": equipment_status_stats,
        "upcoming_interventions": upcoming_interventions,
        "intervention_by_status": intervention_status_stats,
        "unpaid_invoices": unpaid_invoices,
        "current_month_revenue": float(current_month_revenue)
    }
    
    return jsonify(stats), 200
