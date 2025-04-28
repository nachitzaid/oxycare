from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from app.models.invoice import Invoice, InvoiceItem
from app.schemas.invoice_schema import invoice_schema, invoices_schema, invoice_item_schema
from app import db

invoice_bp = Blueprint('invoices', __name__)

@invoice_bp.route('', methods=['GET'])
@jwt_required()
def get_invoices():
    """Get all invoices with filtering options"""
    # Extraction des paramètres de requête pour le filtrage
    patient_id = request.args.get('patient_id')
    statut = request.args.get('statut')
    
    # Requête de base
    query = Invoice.query
    
    # Application des filtres
    if patient_id:
        query = query.filter(Invoice.patient_id == patient_id)
    if statut:
        query = query.filter(Invoice.statut == statut)
    
    # Ordonnancement
    query = query.order_by(Invoice.date_emission.desc())
    
    # Exécution de la requête
    invoices = query.all()
    
    return jsonify(invoices_schema.dump(invoices)), 200

@invoice_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_invoice(id):
    """Get a specific invoice by ID"""
    invoice = Invoice.query.get(id)
    
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404
    
    return jsonify(invoice_schema.dump(invoice)), 200

@invoice_bp.route('', methods=['POST'])
@jwt_required()
def create_invoice():
    """Create a new invoice"""
    try:
        # Extraction et validation des données
        invoice_data = request.get_json()
        if not invoice_data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Extraction des items de facture
        items_data = invoice_data.pop('items', [])
        
        # Validation via Marshmallow
        invoice_data = invoice_schema.load(invoice_data)
        
        # Création de la facture
        invoice = Invoice(**invoice_data)
        db.session.add(invoice)
        db.session.flush()  # Pour obtenir l'ID de la facture
        
        # Ajout des items
        for item_data in items_data:
            item_data['facture_id'] = invoice.id
            invoice_item = InvoiceItem(**item_data)
            db.session.add(invoice_item)
        
        db.session.commit()
        
        return jsonify(invoice_schema.dump(invoice)), 201
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@invoice_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_invoice(id):
    """Update an invoice"""
    try:
        # Vérification si la facture existe
        invoice = Invoice.query.get(id)
        if not invoice:
            return jsonify({"error": "Invoice not found"}), 404
        
        # Extraction et validation des données
        invoice_data = request.get_json()
        if not invoice_data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Extraction des items de facture
        items_data = invoice_data.pop('items', None)
        
        # Validation via Marshmallow
        invoice_data = invoice_schema.load(invoice_data, partial=True)
        
        # Mise à jour des champs de la facture
        for key, value in invoice_data.items():
            setattr(invoice, key, value)
        
        # Gestion des items s'ils sont fournis
        if items_data is not None:
            # Supprimer les items existants
            InvoiceItem.query.filter_by(facture_id=invoice.id).delete()
            
            # Ajouter les nouveaux items
            for item_data in items_data:
                item_data['facture_id'] = invoice.id
                invoice_item = InvoiceItem(**item_data)
                db.session.add(invoice_item)
        
        db.session.commit()
        
        return jsonify(invoice_schema.dump(invoice)), 200
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@invoice_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_invoice(id):
    """Cancel an invoice (change status to 'annulée')"""
    try:
        # Vérification si la facture existe
        invoice = Invoice.query.get(id)
        if not invoice:
            return jsonify({"error": "Invoice not found"}), 404
        
        # Vérification si la facture est déjà payée
        if invoice.est_payee:
            return jsonify({"error": "Cannot cancel a paid invoice"}), 400
        
        # Mise à jour du statut
        invoice.statut = 'annulée'
        db.session.commit()
        
        return jsonify({"message": "Invoice marked as 'annulée'"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

