from scripts.fetch_weather import fetch_weather
from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging
import json


def fetch_and_insert_weather():
    all_data = fetch_weather()  # List of dicts

    if not all_data:
        logging.warning("⚠️ No data returned from fetch_weather")
        return

    hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = hook.get_conn()
    cursor = conn.cursor()

    # Create schema and tables if not exist
    cursor.execute("CREATE SCHEMA IF NOT EXISTS weather;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather.locations (
            id SERIAL PRIMARY KEY,
            city VARCHAR(100),
            region VARCHAR(100),
            country VARCHAR(100),
            lat FLOAT,
            lon FLOAT,
            tz_id TEXT,
            local_time TIMESTAMP
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather.conditions (
            id SERIAL PRIMARY KEY,
            description VARCHAR(100),
            icon_url TEXT,
            code INT
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather.weather_data (
            id SERIAL PRIMARY KEY,
            location_id INT REFERENCES weather.locations(id),
            condition_id INT REFERENCES weather.conditions(id),
            temperature_c FLOAT,
            wind_kph FLOAT,
            humidity INT,
            pressure_mb FLOAT,
            feelslike_c FLOAT,
            uv_index FLOAT,
            gust_kph FLOAT,
            time TIMESTAMP,
            insert_at TIMESTAMP DEFAULT NOW()
        );
    """)

    success_count = 0

    for raw in all_data:
        try:
            location = raw['location']
            current = raw['current']
            condition = current['condition']

            # Insert or get location_id
            cursor.execute("""
                SELECT id FROM weather.locations 
                WHERE city = %s AND region = %s AND country = %s
            """, (location['name'], location['region'], location['country']))
            location_result = cursor.fetchone()

            if location_result:
                location_id = location_result[0]
            else:
                cursor.execute("""
                    INSERT INTO weather.locations (city, region, country, lat, lon, tz_id, local_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
                """, (
                    location['name'], location['region'], location['country'],
                    location['lat'], location['lon'], location['tz_id'], location['localtime']
                ))
                location_id = cursor.fetchone()[0]

            # Insert or get condition_id
            cursor.execute("""
                SELECT id FROM weather.conditions WHERE description = %s AND code = %s
            """, (condition['text'], condition['code']))
            condition_result = cursor.fetchone()

            if condition_result:
                condition_id = condition_result[0]
            else:
                cursor.execute("""
                    INSERT INTO weather.conditions (description, icon_url, code)
                    VALUES (%s, %s, %s) RETURNING id
                """, (
                    condition['text'], condition['icon'], condition['code']
                ))
                condition_id = cursor.fetchone()[0]

            # Insert weather data
            cursor.execute("""
                INSERT INTO weather.weather_data (
                    location_id, condition_id, temperature_c, wind_kph, humidity,
                    pressure_mb, feelslike_c, uv_index, gust_kph, time
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                location_id, condition_id, current['temp_c'], current['wind_kph'], current['humidity'],
                current['pressure_mb'], current['feelslike_c'], current['uv'], current['gust_kph'],
                location['localtime']
            ))

            success_count += 1
            print(f"✅ Inserted data for: {location['name']}")

        except Exception as e:
            logging.error(f"❌ Error processing data for {raw.get('location', {}).get('name', 'UNKNOWN')}: {e}")
            logging.debug(f"Data causing error: {json.dumps(raw, indent=2)}")

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {success_count}/{len(all_data)} records inserted successfully.")
