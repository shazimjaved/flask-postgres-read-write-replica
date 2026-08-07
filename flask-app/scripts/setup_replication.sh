#!/bin/bash

# Note: The schema file may reference PL/pgSQL functions and a payment table 
# partitioned by date range — these load fine in PostgreSQL but our Flask 
# models simplify the payment table to one table for student scope.

echo "Creating replicator user on primary..."
docker exec -i postgres-primary psql -U postgres -c "CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'studentpass';"

echo "Configuring pg_hba.conf on primary for replication..."
docker exec -i postgres-primary bash -c 'echo "host replication replicator all md5" >> /var/lib/postgresql/data/pg_hba.conf'

echo "Reloading primary configuration..."
docker exec -i postgres-primary psql -U postgres -c "SELECT pg_reload_conf();"

echo "Loading Pagila schema into primary database..."
docker exec -i postgres-primary psql -U postgres -d appdb < 1__pagila-schema.sql

echo "Loading Pagila sample data into primary database..."
docker exec -i postgres-primary psql -U postgres -d appdb < 2__pagila-insert-data.sql

echo "Stopping replica..."
docker stop postgres-replica

echo "Running pg_basebackup on the replica..."
# Using an ephemeral container to clear the replica data and clone from primary
docker run --rm --network host -v pgdata-replica:/var/lib/postgresql/data -e PGPASSWORD=studentpass postgres:16 bash -c "rm -rf /var/lib/postgresql/data/* && pg_basebackup -h localhost -p 5432 -U replicator -D /var/lib/postgresql/data -Fp -Xs -R"

echo "Starting replica..."
docker start postgres-replica

echo "Waiting for replica to synchronize..."
sleep 5

echo "Verifying replication by counting films on primary..."
docker exec -i postgres-primary psql -U postgres -d appdb -c "SELECT COUNT(*) FROM film;"

echo "Verifying replication by counting films on replica..."
docker exec -i postgres-replica psql -U postgres -d appdb -c "SELECT COUNT(*) FROM film;"
