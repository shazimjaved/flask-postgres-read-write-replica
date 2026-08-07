# Routes for Rental entities.
from flask import Blueprint, jsonify, request
from app.models.db import Rental
from app.services.db_router import ReadSession, WriteSession
from datetime import datetime

rentals_bp = Blueprint("rentals", __name__, url_prefix="/api/rentals")

@rentals_bp.route("/", methods=["GET"])
def list_rentals():
    customer_id = request.args.get("customer_id")
    session = ReadSession()
    try:
        query = session.query(Rental)
        if customer_id:
            query = query.filter_by(customer_id=customer_id)
            
        rentals = query.limit(50).all()
        return jsonify([
            {
                "rental_id": r.rental_id, 
                "customer_id": r.customer_id, 
                "rental_date": r.rental_date.isoformat() if r.rental_date else None, 
                "return_date": r.return_date.isoformat() if r.return_date else None
            } 
            for r in rentals
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@rentals_bp.route("/", methods=["POST"])
def create_rental():
    data = request.json
    session = WriteSession()
    try:
        new_rental = Rental(
            rental_date=datetime.utcnow(),
            inventory_id=data.get("inventory_id"),
            customer_id=data.get("customer_id"),
            staff_id=data.get("staff_id")
        )
        session.add(new_rental)
        session.commit()
        return jsonify({"message": "Rental created", "rental_id": new_rental.rental_id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@rentals_bp.route("/<int:rental_id>/return", methods=["PUT"])
def mark_rental_returned(rental_id):
    session = WriteSession()
    try:
        rental = session.query(Rental).filter_by(rental_id=rental_id).first()
        if not rental:
            return jsonify({"error": "Rental not found"}), 404
            
        rental.return_date = datetime.utcnow()
        session.commit()
        return jsonify({"message": "Rental returned"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
