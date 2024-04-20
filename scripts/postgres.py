# create_database.py

import os
import sys
import time

import psycopg2


def create_database():
    # PostgreSQL connection parameters
    postgres_host = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port = os.getenv("POSTGRES_PORT", "5432")
    postgres_user = os.getenv("POSTGRES_USER", "your_username")
    postgres_password = os.getenv("POSTGRES_PASSWORD", "your_password")
    postgres_db = os.getenv("POSTGRES_DB", "your_database_name")

    max_attempts = 30  # Number of connection attempts
    attempt_delay = 1  # Delay between attempts in seconds

    attempt = 0
    while attempt < max_attempts:
        try:
            # Connect to PostgreSQL and create the database
            conn = psycopg2.connect(
                host=postgres_host,
                port=postgres_port,
                user=postgres_user,
                password=postgres_password,
                dbname=postgres_db,
            )
            conn.autocommit = True
            cur = conn.cursor()

            # Create the schema if it doesn't exist
            cur.execute("CREATE SCHEMA IF NOT EXISTS shortner;")

            cur.close()
            conn.close()
            print("Database schema created successfully.")
            break  # Exit loop if successful
        except psycopg2.OperationalError as e:
            print(f"Connection attempt {attempt+1}/{max_attempts} failed:", e)
            attempt += 1
            time.sleep(attempt_delay)
    else:
        print("Failed to connect to the database within the timeout period.")
        sys.exit("Exiting...")


if __name__ == "__main__":
    create_database()
