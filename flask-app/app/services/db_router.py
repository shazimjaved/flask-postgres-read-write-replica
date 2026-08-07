import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Writes always go to the primary database. Reads go to the replica database to reduce load on the primary.

# Initialize engines with a small connection pool for student scope
primary_engine = create_engine(os.getenv("PRIMARY_DB_URL"), pool_size=5)
replica_engine = create_engine(os.getenv("REPLICA_DB_URL"), pool_size=5)

# Dedicated session factories for read and write operations
WriteSession = sessionmaker(bind=primary_engine)
ReadSession = sessionmaker(bind=replica_engine)
