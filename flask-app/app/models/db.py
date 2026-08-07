# This file sets up the database connection using SQLAlchemy and defines the database models.

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a database object that can be used across the app
db = SQLAlchemy()

# Represents a country where customers, staff, or stores are located.
class Country(db.Model):
    __tablename__ = 'country'
    country_id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String, nullable=False)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Country {self.country}>"

# Represents a city within a country.
class City(db.Model):
    __tablename__ = 'city'
    city_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.country_id'), nullable=False)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<City {self.city}>"

# Stores physical addresses for customers, staff, and stores.
class Address(db.Model):
    __tablename__ = 'address'
    address_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    address2 = db.Column(db.String, nullable=True)
    district = db.Column(db.String, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'), nullable=False)
    postal_code = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=False)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Address {self.address}>"

# Represents a spoken language for a film (e.g., English, French).
class Language(db.Model):
    __tablename__ = 'language'
    language_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Language {self.name}>"

# Represents a film category or genre (e.g., Action, Comedy).
class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Category {self.name}>"

# Stores details of actors who perform in the films.
class Actor(db.Model):
    __tablename__ = 'actor'
    actor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Actor {self.first_name} {self.last_name}>"

# Represents a movie available for rent.
class Film(db.Model):
    __tablename__ = 'film'
    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    release_year = db.Column(db.Integer, nullable=True)
    language_id = db.Column(db.Integer, db.ForeignKey('language.language_id'), nullable=False)
    rental_duration = db.Column(db.Integer, nullable=False, default=3)
    rental_rate = db.Column(db.Numeric(4, 2), nullable=False, default=4.99)
    length = db.Column(db.Integer, nullable=True)
    replacement_cost = db.Column(db.Numeric(5, 2), nullable=False, default=19.99)
    rating = db.Column(db.String, nullable=False)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Simple relationships
    actors = db.relationship('Actor', secondary='film_actor', backref='films')
    categories = db.relationship('Category', secondary='film_category', backref='films')

    def __repr__(self):
        return f"<Film {self.title}>"

# Link table connecting films to the actors who star in them.
class FilmActor(db.Model):
    __tablename__ = 'film_actor'
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.actor_id'), primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.film_id'), primary_key=True)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<FilmActor actor_id={self.actor_id} film_id={self.film_id}>"

# Link table connecting films to their corresponding categories.
class FilmCategory(db.Model):
    __tablename__ = 'film_category'
    film_id = db.Column(db.Integer, db.ForeignKey('film.film_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), primary_key=True)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<FilmCategory film_id={self.film_id} category_id={self.category_id}>"

# Represents a physical video rental store.
class Store(db.Model):
    __tablename__ = 'store'
    store_id = db.Column(db.Integer, primary_key=True)
    manager_staff_id = db.Column(db.Integer, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.address_id'), nullable=False)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Store {self.store_id}>"

# Represents an employee working at a store.
class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.address_id'), nullable=False)
    email = db.Column(db.String, nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.store_id'), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=True)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Staff {self.first_name} {self.last_name}>"

# Represents a person who rents movies from a store.
class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.store_id'), nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.address_id'), nullable=False)
    activebool = db.Column(db.Boolean, nullable=False, default=True)
    create_date = db.Column(db.Date, nullable=False)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    address = db.relationship('Address')

    def __repr__(self):
        return f"<Customer {self.first_name} {self.last_name}>"

# Tracks specific physical copies of films available in stores.
class Inventory(db.Model):
    __tablename__ = 'inventory'
    inventory_id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.film_id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.store_id'), nullable=False)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Inventory item {self.inventory_id} for film {self.film_id}>"

# Stores movie rental records — links a customer, inventory item, and staff member.
class Rental(db.Model):
    __tablename__ = 'rental'
    rental_id = db.Column(db.Integer, primary_key=True)
    rental_date = db.Column(db.DateTime, nullable=False)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.inventory_id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), nullable=False)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    customer = db.relationship('Customer')
    inventory = db.relationship('Inventory')
    staff = db.relationship('Staff')

    def __repr__(self):
        return f"<Rental {self.rental_id}>"

# Stores individual payment transactions for rentals.
class Payment(db.Model):
    __tablename__ = 'payment'
    payment_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), nullable=False)
    rental_id = db.Column(db.Integer, db.ForeignKey('rental.rental_id'), nullable=False)
    amount = db.Column(db.Numeric(5, 2), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Payment {self.payment_id} amount={self.amount}>"
