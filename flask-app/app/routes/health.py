# Health check routes.
from flask import Blueprint, jsonify
from app.services.db_router import ReadSession
from sqlalchemy import text

health_bp = Blueprint("health", __name__, url_prefix="/")

@health_bp.route("/healthz", methods=["GET"])
def healthz():
    # Simple check that the web server is running
    return jsonify({"status": "ok"}), 200

@health_bp.route("/readyz", methods=["GET"])
def readyz():
    # Check that we can connect to the database
    session = ReadSession()
    try:
        session.execute(text('SELECT 1'))
        return jsonify({"status": "ready"}), 200
    except Exception as e:
        return jsonify({"status": "unavailable", "error": str(e)}), 503
    finally:
        session.close()
