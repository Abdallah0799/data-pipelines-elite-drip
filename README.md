## About the project

<img width="531" alt="image" src="https://github.com/user-attachments/assets/d5033716-c9e2-4537-9b2e-76fcd78902c8">


This project focuses on processing data from a fictive company that operates an e-commerce website selling its own brand of clothing. Unfortunately, the data from this website is quite disorganized. Instead of being centralized, the data is scattered across two main sources: a MongoDB database and CSV files stored in an S3 bucket.

The business teams need easy access to this data to take the best decisions. Therefore, the goal of this project is to efficiently retrieve and consolidate the data from these disparate sources into a centralized BigQuery data warehouse, making it ready for analysis and visualization.

### Built With

**[Python](https://www.python.org/)**: The core programming language for developing the logic and functionality.
**[SQL](https://en.wikipedia.org/wiki/SQL)**: Used for managing and querying relational databases.
**[Google Cloud Platform (GCP)](https://cloud.google.com/)**: For deploying and managing cloud infrastructure.
**[Amazon Web Services (AWS)](https://aws.amazon.com/)**: Leveraged for additional cloud services and scalable solutions.
**[Docker](https://www.docker.com/)**: Containerization platform for packaging and running applications consistently across environments.
**[Kubernetes](https://kubernetes.io/)**: Orchestration system for automating the deployment, scaling, and management of containerized applications.
**[Apache Spark](https://spark.apache.org/)**: Engine for big data processing, supporting large-scale data analytics.


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
