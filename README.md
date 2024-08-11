# Data From a fictive company

This project focuses on processing data from a fictive company that operates an e-commerce website selling its own brand of clothing. Unfortunately, the data from this website is quite disorganized. Instead of being centralized, the data is scattered across two main sources: a MongoDB database and CSV files stored in an S3 bucket.

The business teams need easy access to this data to make informed decisions. Therefore, the goal of this project is to efficiently retrieve and consolidate the data from these disparate sources into a centralized BigQuery data warehouse, making it ready for analysis and visualization.

# 1. Data architecture

The diagram bellow illustrates the data pipelines of this company: 

<img width="751" alt="image" src="https://github.com/user-attachments/assets/33dcfe55-228a-4949-8e69-c500415a897b">

# 2. Infrastructure of the project

