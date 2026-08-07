-- The official Pagila schema already includes some indexes (e.g., idx_fk_customer_id, 
-- idx_fk_address_id, etc. — visible in 1__pagila-schema.sql). 
-- This script adds a few more B-tree indexes specifically tailored to speed up 
-- the queries used by our Flask API for the student demo.

-- 1. B-tree index on rental.customer_id: speeds up "find all rentals for a customer"
CREATE INDEX IF NOT EXISTS idx_api_rental_customer_id ON rental (customer_id);

-- 2. B-tree index on payment.customer_id: speeds up "find all payments for a customer"
CREATE INDEX IF NOT EXISTS idx_api_payment_customer_id ON payment (customer_id);

-- 3. B-tree index on film.title: speeds up searching films by title
CREATE INDEX IF NOT EXISTS idx_api_film_title ON film (title);

-- 4. B-tree index on inventory.film_id: speeds up "find available copies of a film"
CREATE INDEX IF NOT EXISTS idx_api_inventory_film_id ON inventory (film_id);
