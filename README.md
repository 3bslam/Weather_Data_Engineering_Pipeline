# Weather Data Engineering Pipeline
🌦️ Weather Data Engineering Pipeline
📖 Overview
This project demonstrates a complete Data Engineering pipeline for weather data using open-source tools. The pipeline extracts weather data from a public API, stores it in a PostgreSQL database, transforms it using dbt, schedules workflows with Apache Airflow, and finally visualizes the data using Power BI.

The goal is to provide a daily weather summary focused on Egypt, including key metrics like temperature, humidity, and wind speed.

environment

📌 Project Architecture

🔧 System Architecture - Detailed
1. 📥 Data Extraction using Python
A Python script fetches weather data from a public API.


<img width="1920" height="911" alt="data " src="https://github.com/user-attachments/assets/bc6590d0-2baf-4e1f-9a3e-cc4c0a0f36de" />

The data includes: temperature, humidity, wind speed, timestamp, and location.

The script uses libraries like requests and pandas to fetch and process the data.

The script runs daily via Airflow DAG, ensuring automated scheduling and monitoring.

2. 🗃️ Data Storage in PostgreSQL
The processed data is stored in a PostgreSQL database using SQLAlchemy.

Tables created:

weather_data: stores all weather observations.

locations: stores city and country info.

PostgreSQL serves as both the staging and warehouse layer.

3. 🔄 Workflow Orchestration using Airflow
An Airflow DAG schedules and runs:

The data extraction Python script.

A dbt run command to transform the data.

This ensures all steps are automated, reliable, and observable.

4. 🧹 Data Transformation with dbt
dbt models are used to transform and clean raw weather data.

Models include:

stg_weather_data: Staging raw API data.

daily_weather_summary: Aggregated daily summary per city.

Transformations include filtering for Egypt, formatting timestamps, and converting temperature units.

5. 📊 Data Visualization with Power BI
Power BI connects directly to PostgreSQL using Direct Query.

A clean, interactive dashboard displays:

Daily average temperature

Daily average humidity

Wind speed trends

Time series for weather conditions

Filters by city and date allow users to explore specific weather insights for Egypt.



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
