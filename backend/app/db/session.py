import sqlite3
import os
from pathlib import Path
from backend.app import config

DATABASE_PATH = config.DATABASE_PATH

def get_db_connection():
    """Get SQLite database connection with row factory"""
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with schema"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Read and execute schema
    schema_path = Path(__file__).parent / "schema.sql"
    with open(schema_path, 'r') as f:
        schema = f.read()
    
    cursor.executescript(schema)
    conn.commit()
    conn.close()
    print(f"Database initialized at {DATABASE_PATH}")

def execute_query(query, params=()):
    """Execute a query and commit"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    lastrowid = cursor.lastrowid
    conn.close()
    return lastrowid

def fetch_one(query, params=()):
    """Fetch single row"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def fetch_all(query, params=()):
    """Fetch all rows"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
