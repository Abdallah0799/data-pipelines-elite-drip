## About the project

<p align="center">
<img width="326" alt="image" src="https://github.com/user-attachments/assets/5019c4a5-804e-4d34-bde2-8bd362024060" style="border-radius: 10px;">
</p>

Elite Drip is a unique clothing brand exclusively catering to NBA players. Unlike typical clothing companies, Elite Drip has built a brand centered entirely around basketball, creating a community that serves professional basketball players. They operate solely through their e-commerce platform, which launched in January 2023, without any physical stores.

As they enter 2024, the company is shifting its strategy to become data-driven, aiming to optimize its processes and make informed decisions. I have been brought on board as their new Data Engineer to lead this initiative. The challenge ahead is significant, as the company’s data is currently disorganized and scattered across multiple sources, including a MongoDB database, CSV files stored in an S3 bucket, and the [BallDontLie](https://www.balldontlie.io/) database. (PS: don't worry they fired the former web developer)

The business teams need continuous access to high-quality data to make the best decisions. Therefore, the goal of this project is to efficiently retrieve and consolidate the data from these disparate sources into a centralized data warehouse, making it ready for analysis and visualization.

## 🚀 Built With

Languages:
- ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white&style=flat-square) **[Python](https://www.python.org/)**: The core programming language for developing the logic and functionality.
- ![SQL](https://img.shields.io/badge/-SQL-CC2927?logo=Microsoft-SQL-Server&logoColor=white&style=flat-square) **[SQL](https://en.wikipedia.org/wiki/SQL)**: Used for building data transformations in our data warehouse.

Modern Data Tools:
- ![Airflow](https://img.shields.io/badge/-Apache%20Airflow-017CEE?logo=apache-airflow&logoColor=white&style=flat-square) **[Apache Airflow](https://airflow.apache.org/)**: Orchestrator.
- ![dbt](https://img.shields.io/badge/-dbt-FF694B?logo=dbt&logoColor=white&style=flat-square) **[dbt](https://www.getdbt.com/)**: Data transformation tool that allows analysts and engineers to transform, test, and document data.

Cloud:
- ![GCP](https://img.shields.io/badge/-GCP-4285F4?logo=google-cloud&logoColor=white&style=flat-square) **[Google Cloud Platform (GCP)](https://cloud.google.com/)**: We used two services: BigQuery to store our data warehouse and Cloud Storage to store tempory data.
- ![AWS](https://img.shields.io/badge/-AWS-232F3E?logo=amazon-aws&logoColor=white&style=flat-square) **[Amazon Web Services (AWS)](https://aws.amazon.com/)**: We used on service: S3 to store raw data.
- ![MongoDB](https://img.shields.io/badge/-MongoDB-47A248?logo=mongodb&logoColor=white&style=flat-square) **[MongoDB](https://www.mongodb.com/)**: NoSQL database known for its flexibility and scalability, used for managing large volumes of unstructured data.

Devops:
- ![Docker](https://img.shields.io/badge/-Docker-2496ED?logo=docker&logoColor=white&style=flat-square) **[Docker](https://www.docker.com/)**: Containerization platform for packaging and running applications consistently across environments.
- ![Kubernetes](https://img.shields.io/badge/-Kubernetes-326CE5?logo=kubernetes&logoColor=white&style=flat-square) **[Kubernetes](https://kubernetes.io/)** 🏗 Work in progress 🏗

Big Data
- ![Spark](https://img.shields.io/badge/-Apache%20Spark-E25A1C?logo=apachespark&logoColor=white&style=flat-square) **[Apache Spark](https://spark.apache.org/)** 🏗 Work in progress 🏗




# 1. Data modeling Graph

<p align="center">
<img width="756" alt="image" src="https://github.com/user-attachments/assets/5a3b4dbc-37cb-402f-98ff-4af3b3f672d3">
</p>

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
