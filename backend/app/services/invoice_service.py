from app.models.invoice import Invoice, InvoiceItem
from app.models.intervention import Intervention
from app.models.equipment_rental import EquipmentRental
from app.models.patient import Patient
from app import db
from datetime import datetime, timedelta
import uuid

class InvoiceService:
    @staticmethod
    def generate_invoice_number():
        """
        Génère un numéro de facture unique
        """
        prefix = "F-"
        date_part = datetime.now().strftime("%Y%m")
        unique_part = str(uuid.uuid4().int)[:6]
        return f"{prefix}{date_part}-{unique_part}"
    
    @staticmethod
    def create_invoice(invoice_data, items_data=None):
        """
        Crée une nouvelle facture avec ses items
        """
        # Générer un numéro de facture si non fourni
        if not invoice_data.get('numero_facture'):
            invoice_data['numero_facture'] = InvoiceService.generate_invoice_number()
        
        # Créer la facture
        invoice = Invoice(**invoice_data)
        db.session.add(invoice)
        db.session.flush()  # Pour obtenir l'ID de la facture
        
        # Ajouter les items
        if items_data:
            for item_data in items_data:
                item_data['facture_id'] = invoice.id
                invoice_item = InvoiceItem(**item_data)
                db.session.add(invoice_item)
        
        db.session.commit()
        
        return invoice
    
    @staticmethod
    def update_invoice(invoice_id, invoice_data, items_data=None):
        """
        Met à jour une facture et ses items
        """
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            raise ValueError("Facture non trouvée")
        
        # Vérifier si la facture est déjà payée
        if invoice.est_payee and invoice_data.get('statut') != 'payée':
            raise ValueError("Impossible de modifier une facture déjà payée")
        
        # Mettre à jour la facture
        for key, value in invoice_data.items():
            setattr(invoice, key, value)
        
        # Gérer les items si fournis
        if items_data is not None:
            # Supprimer les items existants
            InvoiceItem.query.filter_by(facture_id=invoice.id).delete()
            
            # Ajouter les nouveaux items
            for item_data in items_data:
                item_data['facture_id'] = invoice.id
                invoice_item = InvoiceItem(**item_data)
                db.session.add(invoice_item)
        
        db.session.commit()
        
        return invoice
    
    @staticmethod
    def mark_invoice_as_paid(invoice_id, payment_data):
        """
        Marque une facture comme payée
        """
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            raise ValueError("Facture non trouvée")
        
        if invoice.est_payee:
            raise ValueError("Cette facture est déjà payée")
        
        invoice.statut = 'payée'
        invoice.date_paiement = payment_data.get('date_paiement', datetime.now().date())
        invoice.methode_paiement = payment_data.get('methode_paiement')
        invoice.reference_paiement = payment_data.get('reference_paiement')
        
        db.session.commit()
        
        return invoice
    
    @staticmethod
    def generate_invoice_from_interventions(patient_id, intervention_ids, invoice_data=None):
        """
        Génère une facture à partir d'interventions
        """
        # Vérifier si le patient existe
        patient = Patient.query.get(patient_id)
        if not patient:
            raise ValueError("Patient non trouvé")
        
        # Récupérer les interventions
        interventions = Intervention.query.filter(
            Intervention.id.in_(intervention_ids),
            Intervention.patient_id == patient_id,
            Intervention.facturable == True
        ).all()
        
        if not interventions:
            raise ValueError("Aucune intervention facturable trouvée")
        
        # Préparer les données de base de la facture
        if not invoice_data:
            invoice_data = {}
        
        today = datetime.now().date()
        invoice_data.update({
            'patient_id': patient_id,
            'numero_facture': InvoiceService.generate_invoice_number(),
            'date_emission': today,
            'date_echeance': today + timedelta(days=30),
            'statut': 'en attente',
            'periode_debut': min(i.date_planifiee.date() for i in interventions),
            'periode_fin': max(i.date_fin.date() if i.date_fin else i.date_planifiee.date() for i in interventions)
        })
        
        # Calculer les montants
        montant_ht = sum(i.montant or 0 for i in interventions)
        taux_tva = invoice_data.get('taux_tva', 20.0)
        montant_ttc = montant_ht * (1 + taux_tva/100)
        
        invoice_data.update({
            'montant_ht': montant_ht,
            'montant_ttc': montant_ttc
        })
        
        # Créer les items de facture
        items_data = []
        for intervention in interventions:
            items_data.append({
                'description': f"Intervention {intervention.type_intervention} du {intervention.date_planifiee.strftime('%d/%m/%Y')}",
                'quantite': 1,
                'prix_unitaire': intervention.montant or 0,
                'montant_total': intervention.montant or 0,
                'intervention_id': intervention.id
            })
        
        # Créer la facture
        invoice = InvoiceService.create_invoice(invoice_data, items_data)
        
        # Mettre à jour les interventions avec l'ID de la facture
        for intervention in interventions:
            intervention.facture_id = invoice.id
        
        db.session.commit()
        
        return invoice