from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("SUPABASE_HOST"),
    "port": os.getenv("SUPABASE_PORT"),
    "dbname": os.getenv("SUPABASE_DB"),
    "user": os.getenv("SUPABASE_USER"),
    "password": os.getenv("SUPABASE_PASSWORD"),

} # Database configuration for connecting to Supabase


JWT_SECRET = os.getenv("JWT_SECRET") # JWT secret key for encoding/decoding tokens