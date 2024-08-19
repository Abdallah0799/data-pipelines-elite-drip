## About the project

<img width="531" alt="image" src="https://github.com/user-attachments/assets/d5033716-c9e2-4537-9b2e-76fcd78902c8">


This project focuses on processing data from a fictive company that operates an e-commerce website selling its own brand of clothing. Unfortunately, the data from this website is quite disorganized. Instead of being centralized, the data is scattered across two main sources: a MongoDB database and CSV files stored in an S3 bucket.

The business teams need easy access to this data to take the best decisions. Therefore, the goal of this project is to efficiently retrieve and consolidate the data from these disparate sources into a centralized BigQuery data warehouse, making it ready for analysis and visualization.

### Built With

Languages
<img src="[path/to/image.png](https://github.com/user-attachments/assets/51f468d4-586b-4608-bc08-1b23879c55b5)" alt="Alt text" width="500" height="300">
![image](https://github.com/user-attachments/assets/fc45f7d8-899d-46e0-ae91-5416ca797f7b)

Modern Data Tools
![image](https://github.com/user-attachments/assets/6f695219-fe6c-4b08-812e-cff24ff8af49)
![image](https://github.com/user-attachments/assets/7a4406f7-dec9-450b-bd61-1d1e77303e18)

Cloud
![image](https://github.com/user-attachments/assets/ce00c182-5c02-4350-87b6-9c0b417ecfee)
![image](https://github.com/user-attachments/assets/50dde161-ace3-4307-9636-37f4753dd13b)

Devops
![image](https://github.com/user-attachments/assets/95f44ffc-c76f-45b8-832d-e76ce451db0a)
![image](https://github.com/user-attachments/assets/366098c6-f3bb-4757-b419-c833baf329e2)

Big Data
![image](https://github.com/user-attachments/assets/f370ae47-a006-40f3-b8ce-65188eaadbd5)


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
