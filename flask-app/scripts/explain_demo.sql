-- This script provides an EXPLAIN ANALYZE example using a real Pagila-style query.
-- Run this in psql or pgAdmin after running create_indexes.sql to see how 
-- PostgreSQL utilizes the index to quickly locate a specific customer's rentals 
-- instead of performing a sequential scan over the entire table.

EXPLAIN ANALYZE SELECT * FROM rental WHERE customer_id = 1;
