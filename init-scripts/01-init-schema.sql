-- Create database if not exists
CREATE DATABASE open_meteo;

-- Connect to the database
\c open_meteo;

-- Grant privileges to Airflow user
GRANT CONNECT ON DATABASE open_meteo TO airflow;
GRANT USAGE ON SCHEMA public TO airflow;

-- Allow Airflow to create and drop tables
GRANT CREATE, DROP ON SCHEMA public TO airflow;

-- Allow Airflow to SELECT, INSERT, UPDATE, DELETE on all current and future tables
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO airflow;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO airflow;

-- Allow Airflow to create and use sequences (needed for serial primary keys)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO airflow;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT USAGE, SELECT ON SEQUENCES TO airflow;
