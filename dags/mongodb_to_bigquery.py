from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from importlib import import_module
from datetime import datetime

from data_engineering.api_connectors.mongodb import MongoDbConnector
from data_engineering.api_connectors.bigquery import BigQueryConnector
import settings

# Default DAG arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 8, 6),
    "retries": 1,
}

with DAG(
    "mongodb_to_bigquery",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:

    mongodb_collections_to_fetch = ["orders", "products"]
    mongo_filters = {
        #"updatedAt": {"$gte": datetime.now() - timedelta(2 / 24)}
    }
    mongodb_connector = MongoDbConnector("center")
    bigquery_connector = BigQueryConnector(service_account_infos=settings.SERVICE_ACCOUNT_BQ_ADMIN)

    for collection in mongodb_collections_to_fetch:
        # Getting the coresponding BQ schema
        module = import_module('data_engineering.data_schemas.' + collection)
        schema = getattr(module, collection + '_schema')

        # Extract Task
        extract_task = PythonOperator(
            task_id=f"extract_{collection}",
            python_callable=mongodb_connector.fetch_data,
            op_args=[collection, mongo_filters],
            provide_context=True,
            do_xcom_push=True,
            dag=dag,
        )

        # Load Task
        load_task = PythonOperator(
            task_id=f"load_{collection}",
            python_callable=bigquery_connector.insert_data,
            op_kwargs={"data": extract_task.output,
                       "dataset_id": "fictive_company",
                       "table_name": collection,
                       "schema": schema,
                       "duplicate_columns": ["id"],
                       "order_columns": ["id"]},
            provide_context=True,
            dag=dag
        )

        # Setting taks dependencies
        extract_task >> load_task
