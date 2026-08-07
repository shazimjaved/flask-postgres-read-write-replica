# Routes for Customer entities.
from flask import Blueprint, jsonify, request
from app.models.db import Customer
from app.services.db_router import ReadSession, WriteSession
from datetime import date

customers_bp = Blueprint("customers", __name__, url_prefix="/api/customers")

@customers_bp.route("/", methods=["GET"])
def list_customers():
    session = ReadSession()
    try:
        customers = session.query(Customer).filter_by(activebool=True).limit(50).all()
        return jsonify([
            {"customer_id": c.customer_id, "first_name": c.first_name, "last_name": c.last_name} 
            for c in customers
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@customers_bp.route("/", methods=["POST"])
def register_customer():
    data = request.json
    session = WriteSession()
    try:
        new_customer = Customer(
            store_id=data.get("store_id", 1),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            address_id=data.get("address_id", 1),
            activebool=True,
            create_date=date.today()
        )
        session.add(new_customer)
        session.commit()
        return jsonify({"message": "Customer registered", "customer_id": new_customer.customer_id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@customers_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    session = ReadSession()
    try:
        customer = session.query(Customer).filter_by(customer_id=customer_id).first()
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        
        address_info = customer.address.address if customer.address else "Unknown"
        
        return jsonify({
            "customer_id": customer.customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "address": address_info
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@customers_bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    data = request.json
    session = WriteSession()
    try:
        customer = session.query(Customer).filter_by(customer_id=customer_id).first()
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
            
        if "email" in data:
            customer.email = data["email"]
        if "activebool" in data:
            customer.activebool = data["activebool"]
            
        session.commit()
        return jsonify({"message": "Customer updated"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
