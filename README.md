# **Open-Meteo Import Pipeline**

This data pipeline imports weather data from the official **Open-Meteo API**.  
It extracts **hourly weather data** (including temperature, wind speed, and total precipitation) for **New York City, Los Angeles, and San Francisco**.  
The data is then saved into two separate tables with predefined column structures.

The pipeline is scheduled to run **daily** using **Apache Airflow**.

---

## **📁 Folder Structure**

- **`import_dags/`** – Stores Airflow DAGs. This folder is copied into the Docker container.
- **`import_open_meteo/`** – Contains Python scripts for **extracting, transforming, and loading (ETL)** the data.
- **`init-scripts/`** – Contains initialization scripts for creating a dedicated **PostgreSQL database** for Open-Meteo data and applying necessary grants.
- **`postgres_files/`** – Contains two `.csv` files, each exported from the respective PostgreSQL tables.
- **`docker-compose.yml`** – Docker Compose configuration file.
- **`README.md`** – This documentation file.

---

## **✅ Prerequisites**

Before running the pipeline, ensure you have the following installed:

1. **Docker**

---

## **🚀 How to Run the Pipeline**

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   ```
2. **Navigate to the project folder:**
   ```sh
   cd hcvt
   ```
3. **Build and start the Docker containers:**
   ```sh
   docker-compose build --no-cache
   docker-compose up
   ```
4. **Verify that the containers are running** in **Docker Dashboard**:
   - **First container** → PostgreSQL database
   - **Second container** → Apache Airflow

5. **Open Airflow UI in your browser:**
   ```
   http://0.0.0.0:8080/dags/weather_etl/grid
   ```
6. **Log in to Airflow:**
   - **Username:** `admin`
   - **Password:** `admin`

7. **Check the DAGs page** – if everything is set up correctly, the DAG will start automatically and begin **extracting, transforming, and loading data**.

---

## **📌 Pipeline Specifications**

1. The **Extract, Transform, and Load (ETL) steps** are implemented as separate tasks in **Airflow**.
   - This structure allows for **task dependency management** within Airflow.
2. After the **Extract & Transform** steps, the data is stored in the **file system (`/hcvt/import_open_meteo/fs`)**.
   - This ensures **data separation**, enabling **backfilling** when needed.

---

## **🛠️ Future Improvements**

1. **Add unit tests** for data validation.
2. **Implement type annotations and linting** for better code quality.
3. **Enhance logging** to improve debugging.
4. **Secure credentials** (move them to environment variables or secrets manager).
5. **Add monitoring & metrics** to track pipeline performance.
6. **Improve Airflow monitoring** by integrating with Prometheus/Grafana.

---
