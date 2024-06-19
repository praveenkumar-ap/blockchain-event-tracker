# Blockchain Event Tracker

## Overview

This project tracks `UserOperationEvent` on the EntryPoint contract on the Polygon or Base Mainnet blockchain, stores the data in a MySQL database, and visualizes it using Grafana.

## Prerequisites

- Docker
- Docker Compose
- Python 3.x

## Setup

1. Clone the repository:

   
   git clone https://github.com/yourusername/user-operation-tracker.git
   cd user-operation-tracker

2. Install required libraries
   
   pip install -r requirements.txt

3. Start the Docker containers: 
   docker-compose up -d

4. Run the MySQL schema setup: 
   docker exec -i <mysql_container_id> mysql -uuser -ppassword blockchain < schema.sql

5. Run the event tracker:
   python track_events.py

6. Process the data:
   python process_data.py

Grafana Dashboard
Log in to Grafana at http://localhost:3000 with the default credentials (admin/admin).

Add a MySQL data source with the following details:

Host: mysql:3306
Database: blockchain
User: user
Password: password
Create a new dashboard and add panels to visualize the data.


Detailed Steps to Create the Grafana Dashboard
Access Grafana:

Open your browser and navigate to http://localhost:3000.
Log in with admin / admin (or the password you set).
Add MySQL Data Source:

Navigate to Configuration > Data Sources.
Click Add data source and select MySQL.
Fill in the details:
Host: mysql:3306
Database: blockchain.
User: user.
Password: password
Click Save & Test to verify the connection.
Create a New Dashboard:

Go to the Dashboards menu.
Click + and select Dashboard.
Click Add new panel.
Configure the Panel:

In the Query section, select the MySQL data source.
Enter the below query in block

SELECT
  $__timeGroupAlias(timestamp, '5m'), -- Group by time (every 5 minutes)
  COUNT(*) AS count,
  CASE
    WHEN is_biconomy = 1 THEN 'Biconomy Bundlers'
    ELSE 'Other Bundlers'
  END AS bundler_type
FROM
  user_operations
GROUP BY
  $__timeGroup(timestamp, '5m'), -- Group by time (every 5 minutes)
  is_biconomy
ORDER BY
  $__timeGroup(timestamp, '5m') -- Order by time


Configure the Visualization:

In the Visualization tab, choose a suitable chart type, such as Time series.
Configure the visualization options as needed (e.g., legend, axes, tooltips).
Apply and Save the Dashboard:

Click Apply to save the panel.
Click Save dashboard to save the entire dashboard.

 
































