# Energy Data Analysis and Visualization

## Overview
In this assignment, you will demonstrate your skills in data engineering by performing tasks that include data collection, manipulation, analysis, and visualization. You will work with energy-related data, collected from various APIs, to create an insightful data pipeline and visualization.

## Objectives
- Collect and clean data from different APIs related to energy (e.g., electricity consumption, renewable energy sources, etc.).
- Analyze the data to extract meaningful insights.
- Automate the data pipeline using Argo Workflow (or Airflow)
- Store and manipulate data using SQLAlchemy and PostGIS.
- Transform data using dbt.
- Visualize the results using Superset or a similar tool. (Optional)

## Tasks
### Part 1: Data Collection and Manipulation
Write a Python script to scrape data from at least two different energy-related APIs.
- Clean and preprocess the data using Pandas
- Perform exploratory analysis to understand the data
- Use scikit-learn to create a simple model based on the dataset

### Part 2: Workflow Automation
Automate the data pipeline created in Task 1 using workflow tool.
- Define the workflow to automate data collection, cleaning and analysis.
- Ensure the workflow is robust and can handle potential failures.

### Part 3: Database Operations
Store the cleaned data in a PostgreSQL database using SQLAlchemy. Include a spatial data processing task 
using PostGIS.
- Design a database schema suitable for the data.
- Write SQLAlchemy code to store and query the data.
- Perform at least one geospatial query or operation using PostGIS. (If any)

### Part 4: Data Transformation and Testing
Use dbt to transform the stored data into a format suitable for analysis and reporting.
- Create dbt models to transform raw data into a star schema.
- Write tests in dbt to ensure the integrity of the transformations (Optional)

### Part 5: Visualization (Optional)
Create a dashboard in Apache Superset (or a similar tool) to visualize the insights from your data.
- The dashboard should contain at least three different types of visualizations (e.g., bar chart, line 
graph, map)
- Visualizations should provide meaningful insights into the energy data.

## Deliverables
- Documentation about how to use the solution
- A diagram illustrating the data pipeline workflow.


