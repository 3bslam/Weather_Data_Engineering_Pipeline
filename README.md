# Weather Data Engineering Pipeline

This project uses Apache Airflow (via Docker Compose) to orchestrate a weather data pipeline.

## Setup

1. **Set your OpenWeatherMap API Key:**
   - Edit `dags/weather_data_pipeline.py` and replace `YOUR_OPENWEATHERMAP_API_KEY` with your actual API key.
   - You can get a free API key from https://openweathermap.org/api

2. **Start Airflow with Docker Compose:**
   - Open a terminal in this project directory.
   - Run:
     ```sh
     docker-compose up
     ```
   - The Airflow web UI will be available at [http://localhost:8080](http://localhost:8080)

3. **Access Airflow:**
   - Default username: `airflow`
   - Default password: `airflow`

4. **Trigger the DAG:**
   - In the Airflow UI, enable and trigger the `weather_data_pipeline` DAG.

## Notes
- The weather data will be saved to `/opt/airflow/data/weather.json` inside the webserver/scheduler containers.
- You can add more tasks to the DAG for further processing, storage, or analytics. 