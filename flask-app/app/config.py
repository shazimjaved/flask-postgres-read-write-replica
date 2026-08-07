# This file loads configuration settings from environment variables.

import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

class Config:
    # Set the secret key for the application
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    # Set the primary database URL
    PRIMARY_DB_URL = os.getenv("PRIMARY_DB_URL")
    # Set the replica database URL
    REPLICA_DB_URL = os.getenv("REPLICA_DB_URL")
