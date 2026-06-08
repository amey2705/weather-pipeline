import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database="weather_db",
        user="postgres",
        password=DB_PASSWORD
    )

def create_summary_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS daily_summary (
            date DATE,
            city TEXT,
            avg_temp FLOAT,
            max_temp FLOAT,
            min_temp FLOAT,
            avg_humidity FLOAT,
            PRIMARY KEY (date, city)
        )
    """)

def transform():
    """Aggregate raw weather data into daily summaries"""
    conn = get_db_connection()
    cur = conn.cursor()

    create_summary_table(cur)

    # Delete today's summary so we can recompute it fresh
    cur.execute("DELETE FROM daily_summary WHERE date = CURRENT_DATE")

    # Aggregate raw data into daily summary
    cur.execute("""
        INSERT INTO daily_summary (date, city, avg_temp, max_temp, min_temp, avg_humidity)
        SELECT
            DATE(timestamp)       AS date,
            city,
            ROUND(AVG(temperature)::numeric, 2) AS avg_temp,
            MAX(temperature)      AS max_temp,
            MIN(temperature)      AS min_temp,
            ROUND(AVG(humidity)::numeric, 2)    AS avg_humidity
        FROM raw_weather
        WHERE DATE(timestamp) = CURRENT_DATE
        GROUP BY DATE(timestamp), city
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Transformation complete — daily_summary updated")

if __name__ == "__main__":
    transform()
