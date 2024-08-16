from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.task_group import TaskGroup
from typing import List

from data_engineering.schemas import BigQuerySchemas
from data_engineering.api_connectors.bigquery import BigQueryConnector
from utils import get_data_types_to_fetch

import settings


bigquery_schemas = BigQuerySchemas()
bigquery_conn = BigQueryConnector(settings.SERVICE_ACCOUNT_BQ_ADMIN)


def get_pipeline_task_group(
        connector,
        dag: DAG,
        op_kwargs_extract: dict
) -> TaskGroup:
    """
    """
    task_groupe_name = connector.name + '_to_bq'
    data_names = get_data_types_to_fetch(connector.name,
                                         connector.dataset)

    # Build task
    with TaskGroup(task_groupe_name) as task_group:
        for data_name in data_names:
            # Getting the coresponding BQ schema
            schema = getattr(bigquery_schemas, data_name)

            # Building op_kwargs
            op_kwargs = {**{"data_type": data_name}, **op_kwargs_extract}

            # Extract Task
            extract_task = PythonOperator(
                task_id=f"extract_{data_name}",
                python_callable=connector.fetch_data,
                op_kwargs=op_kwargs,
                provide_context=True,
                do_xcom_push=True,
                dag=dag,
            )

            # Load Task
            load_task = PythonOperator(
                task_id=f"load_{data_name}",
                python_callable=bigquery_conn.insert_data,
                op_kwargs={
                    "data": extract_task.output,
                    "dataset_id": "fictive_company",
                    "table_name": data_name,
                    "schema": schema,
                    "duplicate_columns": ["id"],
                    "order_columns": ["id"],
                },
                provide_context=True,
                dag=dag,
            )

            # Setting taks dependencies
            extract_task >> load_task

    return task_group
