## About the project

<p align="center">
<img width="326" alt="image" src="https://github.com/user-attachments/assets/5019c4a5-804e-4d34-bde2-8bd362024060" style="border-radius: 10px;">
</p>

Elite Drip is a unique clothing brand exclusively catering to NBA players. Unlike typical clothing companies, Elite Drip has built a brand centered entirely around basketball, creating a community that serves professional basketball players. They operate solely through their e-commerce platform, which launched in January 2023, without any physical stores.

As they enter 2024, the company is shifting its strategy to become data-driven, aiming to optimize its processes and make informed decisions. I have been brought on board as their new Data Engineer to lead this initiative. The challenge ahead is significant, as the company’s data is currently disorganized and scattered across multiple sources, including a MongoDB database, CSV files stored in an S3 bucket, and the [BallDontLie](https://www.balldontlie.io/) database. (PS: don't worry they fired the former web developer)

The business teams need continuous access to high-quality data to make the best decisions. Therefore, the goal of this project is to efficiently retrieve and consolidate the data from these disparate sources into a centralized data warehouse, making it ready for analysis and visualization.

## Table of Contents
[Built with](#🚀-built-with)
1. [Data modeling Graph](#data-modeling-graph)
2. [Data architecture](#data-architecture)
3. [Data Visualization](#data-visualization)
4. [Infrastructure](#infrastructure)
5. [Big Data processing](#big-data-processing)

[About the data](#about-the-data)


## 🚀 Built With

Languages:
- ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white&style=flat-square) **[Python](https://www.python.org/)**: The core programming language for developing the logic and functionality.
- ![SQL](https://img.shields.io/badge/-SQL-CC2927?logo=Microsoft-SQL-Server&logoColor=white&style=flat-square) **[SQL](https://en.wikipedia.org/wiki/SQL)**: Used for building data transformations in our data warehouse.

Modern Data Tools:
- ![Airflow](https://img.shields.io/badge/-Apache%20Airflow-017CEE?logo=apache-airflow&logoColor=white&style=flat-square) **[Apache Airflow](https://airflow.apache.org/)**: Orchestrator.
- ![dbt](https://img.shields.io/badge/-dbt-FF694B?logo=dbt&logoColor=white&style=flat-square) **[dbt](https://www.getdbt.com/)**: Data transformation tool used to transform, test, and document data.

Cloud:
- ![GCP](https://img.shields.io/badge/-GCP-4285F4?logo=google-cloud&logoColor=white&style=flat-square) **[Google Cloud Platform (GCP)](https://cloud.google.com/)**
- ![AWS](https://img.shields.io/badge/-AWS-232F3E?logo=amazon-aws&logoColor=white&style=flat-square) **[Amazon Web Services (AWS)](https://aws.amazon.com/)**

No-SQL Database:
- ![MongoDB](https://img.shields.io/badge/-MongoDB-47A248?logo=mongodb&logoColor=white&style=flat-square) **[MongoDB](https://www.mongodb.com/)**

Devops:
- ![Docker](https://img.shields.io/badge/-Docker-2496ED?logo=docker&logoColor=white&style=flat-square) **[Docker](https://www.docker.com/)**
- ![Kubernetes](https://img.shields.io/badge/-Kubernetes-326CE5?logo=kubernetes&logoColor=white&style=flat-square) **[Kubernetes](https://kubernetes.io/)** 🏗 Work in progress 🏗

Big Data
- ![Spark](https://img.shields.io/badge/-Apache%20Spark-E25A1C?logo=apachespark&logoColor=white&style=flat-square) **[Apache Spark](https://spark.apache.org/)** 🏗 Work in progress 🏗




## Data modeling Graph

<p align="center">
<img width="756" alt="image" src="https://github.com/user-attachments/assets/5a3b4dbc-37cb-402f-98ff-4af3b3f672d3">
</p>

## Data architecture

To design the data architecture, I will implement an ELT (Extract, Load, Transform) pipeline using Python. The process begins by extracting data from our three sources, followed by loading it into a BigQuery Data Warehouse. Finally, we will transform the data within the Data Warehouse using dbt. These three core tasks will be orchestrated with Apache Airflow. The diagram below illustrates the data pipelines:

<p align="center">
<img width="756" alt="image" src="https://github.com/user-attachments/assets/6c1cb846-b202-488d-a084-308497826a6e">
</p>

1. **Extract task**

To accomplish this task, we will need to interact with the source databases via API calls. To facilitate this, I developed a set of connector classes: MongoDBConnector, S3Connector, and BallDontLieConnector. Each of these classes inherits from a BaseConnector class and includes a fetch_data method. This method accepts two key parameters: data_type (representing the specific entity to fetch, such as orders or order items) and filters (which can include criteria like date ranges).

2. **Load task**

To load the extracted data into BigQuery, we'll need to interact with it via API calls. For this purpose, I developed a BigQueryConnector class. This class includes an insert_data method, which manages duplicates to ensure that the BigQuery table remains free of redundant entries. The method requires you to specify an order field, which it uses to determine the preferred entry among duplicates for a particular field.

3. **Transform task**

Finally, a dbt task is initiated to transform our raw tables into models that are ready for analysis and visualization. This task is orchestrated using the open-source dbt-airflow project, ensuring a seamless integration between dbt and our Airflow pipeline


### About Airflow
There is a single [DAG](https://github.com/Abdallah0799/data-pipelines-elite-drip/blob/main/dags/run_pipeline.py) scheduled to run every hour. It includes three Task Group that run in parallel. These Task Group contain two tasks: an extract task from the source and a load task to the data warehouse. In order to communicate data between these two tasks, I store the extracted data as a csv file in a Cloud Storage bucket then retrieve this file in the load task. Here are the 3 Tasks Group: 
- fetching data from **MongoDB** and loading it into BigQuery
- fetching data from **S3** and loading it into BigQuery
- fetching data from **BallDontLie** and loading it into BigQuery

Once these 3 tasks successfully complete, the final task is triggered to execute our dbt models. 

Here is the tasks diagram:

<p align="center">
<img width="600" alt="image" src="https://github.com/user-attachments/assets/d696ba56-1721-430e-8171-083acfbb82eb">
</p>

## Data Visualization
We will use Looker Studio for data Visualization.

<p align="left">
<img width="120" alt="image" src="https://github.com/user-attachments/assets/d9386285-2a9c-4a51-a0b1-221d682dd0e8">
</p>

Here is the link to the [dashboard](https://lookerstudio.google.com/reporting/074e01b7-80d1-471e-b25e-fe0f8b4f36bd/page/4Z25D).

## Infrastructure
🏗 Work in progress 🏗

The ultimate goal is to deploy my Airflow application on Google Kubernetes Engine (GKE). But, as you might expect, it's not that straightforward 😅. So, for now, we’ll simulate a Kubernetes cluster locally using Kind and deploy Airflow on it. The local application will get the DAGS and the rest of this repo with Git-sync. The DevOps settings (like the Helm chart and Dockerfile) are housed in a separate [repository](https://github.com/Abdallah0799/airflow-k8s). This setup will communicate with our main repo via Git-sync. Detailed instructions will be provided in the other repo, allowing you to build your cluster locally and launch the Airflow app.

## Big Data processing
🏗 Work in progress 🏗

A new source of data will be added to the pipeline. This source will have a big volume of data, that we will need to process with spark before loading it to our warehouse.

## About the data

The data from **orders**, **order_items** and **charges** have been genrated randomly.

The data from **products** have been created manually. I will developp later an API to generate new products with LLM.

The data from **players** is provides by the BallDontLie api.

