# Routes for Film entities.
from flask import Blueprint, jsonify, request
from app.models.db import Film, Category
from app.services.db_router import ReadSession, WriteSession

films_bp = Blueprint("films", __name__, url_prefix="/api/films")

@films_bp.route("/", methods=["GET"])
def list_films():
    category_name = request.args.get("category")
    session = ReadSession()
    try:
        query = session.query(Film)
        if category_name:
            query = query.join(Film.categories).filter(Category.name == category_name)
        
        films = query.limit(50).all()
        return jsonify([
            {
                "film_id": f.film_id, 
                "title": f.title, 
                "rental_rate": float(f.rental_rate) if f.rental_rate else 0.0
            } 
            for f in films
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@films_bp.route("/", methods=["POST"])
def add_film():
    data = request.json
    session = WriteSession()
    try:
        new_film = Film(
            title=data.get("title"),
            description=data.get("description"),
            release_year=data.get("release_year"),
            language_id=data.get("language_id", 1),
            rental_duration=data.get("rental_duration", 3),
            rental_rate=data.get("rental_rate", 4.99),
            replacement_cost=data.get("replacement_cost", 19.99),
            rating=data.get("rating", "G")
        )
        session.add(new_film)
        session.commit()
        return jsonify({"message": "Film created", "film_id": new_film.film_id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@films_bp.route("/<int:film_id>", methods=["GET"])
def get_film(film_id):
    session = ReadSession()
    try:
        film = session.query(Film).filter_by(film_id=film_id).first()
        if not film:
            return jsonify({"error": "Film not found"}), 404
        
        return jsonify({
            "film_id": film.film_id,
            "title": film.title,
            "description": film.description,
            "actors": [{"first_name": a.first_name, "last_name": a.last_name} for a in film.actors],
            "categories": [c.name for c in film.categories]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@films_bp.route("/<int:film_id>", methods=["PUT"])
def update_film(film_id):
    data = request.json
    session = WriteSession()
    try:
        film = session.query(Film).filter_by(film_id=film_id).first()
        if not film:
            return jsonify({"error": "Film not found"}), 404
            
        if "rental_rate" in data:
            film.rental_rate = data["rental_rate"]
        if "description" in data:
            film.description = data["description"]
            
        session.commit()
        return jsonify({"message": "Film updated"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@films_bp.route("/<int:film_id>", methods=["DELETE"])
def delete_film(film_id):
    session = WriteSession()
    try:
        film = session.query(Film).filter_by(film_id=film_id).first()
        if not film:
            return jsonify({"error": "Film not found"}), 404
            
        session.delete(film)
        session.commit()
        return jsonify({"message": "Film deleted"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
