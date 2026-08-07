# Routes for Payment entities.
from flask import Blueprint, jsonify, request
from app.models.db import Payment
from app.services.db_router import ReadSession, WriteSession
from datetime import datetime

payments_bp = Blueprint("payments", __name__, url_prefix="/api/payments")

@payments_bp.route("/", methods=["GET"])
def list_payments():
    customer_id = request.args.get("customer_id")
    session = ReadSession()
    try:
        query = session.query(Payment)
        if customer_id:
            query = query.filter_by(customer_id=customer_id)
            
        payments = query.limit(50).all()
        return jsonify([
            {
                "payment_id": p.payment_id, 
                "amount": float(p.amount) if p.amount else 0.0, 
                "payment_date": p.payment_date.isoformat() if p.payment_date else None
            } 
            for p in payments
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@payments_bp.route("/", methods=["POST"])
def record_payment():
    data = request.json
    session = WriteSession()
    try:
        new_payment = Payment(
            customer_id=data.get("customer_id"),
            staff_id=data.get("staff_id"),
            rental_id=data.get("rental_id"),
            amount=data.get("amount"),
            payment_date=datetime.utcnow()
        )
        session.add(new_payment)
        session.commit()
        return jsonify({"message": "Payment recorded", "payment_id": new_payment.payment_id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
