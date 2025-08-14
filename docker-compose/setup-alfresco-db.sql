-- Create the alfresco user and database for Alfresco Community Edition
-- Run this script in your existing PostgreSQL server as a superuser (e.g., postgres)

-- Create the alfresco user if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'alfresco') THEN
    CREATE USER alfresco WITH PASSWORD 'alfresco';
  END IF;
END
$$;

-- Create the alfresco database if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'alfresco') THEN
    CREATE DATABASE alfresco OWNER alfresco ENCODING 'UTF8';
  END IF;
END
$$;

-- Grant all privileges on the database to the alfresco user
GRANT ALL PRIVILEGES ON DATABASE alfresco TO alfresco;

-- Connect to the alfresco database to set up permissions
\c alfresco

-- Grant schema permissions
GRANT ALL ON SCHEMA public TO alfresco;