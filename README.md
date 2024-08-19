## About the project

<img width="531" alt="image" src="https://github.com/user-attachments/assets/d5033716-c9e2-4537-9b2e-76fcd78902c8">


This project focuses on processing data from a fictive company that operates an e-commerce website selling its own brand of clothing. Unfortunately, the data from this website is quite disorganized. Instead of being centralized, the data is scattered across two main sources: a MongoDB database and CSV files stored in an S3 bucket.

The business teams need easy access to this data to take the best decisions. Therefore, the goal of this project is to efficiently retrieve and consolidate the data from these disparate sources into a centralized BigQuery data warehouse, making it ready for analysis and visualization.

### Built With

* ![image](https://github.com/user-attachments/assets/cd1e5ded-8cc6-46f4-9334-509d43f57b10)
* ![image](https://github.com/user-attachments/assets/d1ebfac4-0125-4873-be69-e70110487dd0)
* ![image](https://github.com/user-attachments/assets/cf05dfee-ccc8-4e19-8aa4-1fdf52230c1c)
* ![image](https://github.com/user-attachments/assets/8bed3758-9039-4943-8d8e-1bafefb36c11)
* ![image](https://github.com/user-attachments/assets/de1515d0-7a1b-42c7-896a-b89bb6de2cd3)
* ![image](https://github.com/user-attachments/assets/8b89a7b6-1cd6-41d3-a1d4-6e51201ace84)
* ![image](https://github.com/user-attachments/assets/7b23be9d-81a1-46fd-9c16-30131ebda44b)






# 1. Data modelling 
Here is the data modelling:

# 2. Data architecture

The diagram bellow illustrates the data pipelines of this company: 

<img width="751" alt="image" src="https://github.com/user-attachments/assets/33dcfe55-228a-4949-8e69-c500415a897b">

Airflow will schedule a dag every hour that follows these steps:
- extract the latest data from MongoDB and S3 (typically data having updated_at field change the last hour)
- then load this data into Bigquery table and make sure to not have duplicate and keep only the most recent data in each table
- finally a dbt task is started to make transformation on our raw tables and create models ready for analysis and visualization. dbt task is created with the open source project dbt-airflow
 
<img width="600" alt="image" src="https://github.com/user-attachments/assets/d696ba56-1721-430e-8171-083acfbb82eb">

# 3. Data Visualization
We will use Looker Studio for data Viz
Here is the link to the dashboard: 

# 4. Infrastructure: Deploy Airflow on Google Kubernetes Engine
🏗 Work in progress 🏗

We will deploy airlow on Google Kubernetes Engine.
For the moment we simulate locally a Kubernetes cluster with kind, and deploy Airflow on it.
The helm chart is associated to this project.
You can build airflow locally on a Kubernetes cluster with the following steps:

# 5. Processing Big Volume of data with Spark
🏗 Work in progress 🏗

A new source of data will be added to the pipeline. This source will have a big volume of data, that we will need to process with spark before loading it to our warehouse.

# 6. About the data
