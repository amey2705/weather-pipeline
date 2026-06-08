import requests
import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv
from transformation.transform import validate_record

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PASSWORD = os.getenv("DB_PASSWORD")
CITY = "London"

def fetch_weather():
    """Fetch current weather from OpenWeatherMap API"""
    url = (
    f"https://api.openweathermap.org/data/2.5/weather"
    f"?q={CITY}&appid={API_KEY}&units=metric"
)
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    return {
        "city": CITY,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "weather": data["weather"][0]["description"],
        "timestamp": datetime.utcnow()
    }

def get_db_connection():
    """Create and return a database connection"""
    return psycopg2.connect(
        host=DB_HOST,
        database="weather_db",
        user="postgres",
        password=DB_PASSWORD
    )

def create_table(cur):
    """Create raw_weather table if it doesn't exist"""
    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw_weather (
            id SERIAL PRIMARY KEY,
            city TEXT,
            temperature FLOAT,
            humidity INT,
            wind_speed FLOAT,
            weather TEXT,
            timestamp TIMESTAMP
        )
    """)

def save_to_db(record):
    """Save a weather record to the database"""
    conn = get_db_connection()
    cur = conn.cursor()
    create_table(cur)
    cur.execute("""
        INSERT INTO raw_weather
            (city, temperature, humidity, wind_speed, weather, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        record["city"],
        record["temperature"],
        record["humidity"],
        record["wind_speed"],
        record["weather"],
        record["timestamp"]
    ))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Saved record: {record}")

if __name__ == "__main__":
    record = fetch_weather()
    validate_record(record)
    save_to_db(record)
