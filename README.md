# Data From a fictive company

This project focuses on processing data from a fictive company that operates an e-commerce website selling its own brand of clothing. Unfortunately, the data from this website is quite disorganized. Instead of being centralized, the data is scattered across two main sources: a MongoDB database and CSV files stored in an S3 bucket.

The business teams need easy access to this data to take the best decisions. Therefore, the goal of this project is to efficiently retrieve and consolidate the data from these disparate sources into a centralized BigQuery data warehouse, making it ready for analysis and visualization.

# 1. Data architecture

The diagram bellow illustrates the data pipelines of this company: 

<img width="751" alt="image" src="https://github.com/user-attachments/assets/33dcfe55-228a-4949-8e69-c500415a897b">

Airflow will schedule a dag every hour that follows these steps:
- extract the latest data from MongoDB and S3 (typically data having updated_at field change the last hour)
- then load this data into Bigquery table and make sure to not have duplicate and keep only the most recent data in each table
- finally a dbt task is started to make transformation on our raw tables and create models ready for analysis and visualization. dbt task is created with the open source project dbt-airflow
 

# 2. Data modelling 

# 3. Infrastructure
🏗 Work in progress 🏗
We will deploy airlow on Google Kubernetes Engine.
For the moment we simulate locally a Kubernetes cluster with kind, and deploy Airflow on it.
The helm chart is associated to this project.
You can build airflow locally on a Kubernetes cluster with the following steps:

# 4. Data Visualization
