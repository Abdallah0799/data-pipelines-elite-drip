from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.task_group import TaskGroup
from typing import List

from data_engineering.data_schemas import load_schema
from data_engineering.api_connectors.bigquery import BigQueryConnector
from data_engineering.api_connectors.cloud_storage import CloudStorageConnector
from utils import get_data_types_to_fetch

import settings

# define the bigquery connector
bigquery_conn = BigQueryConnector("fictive_company",
                                  settings.SERVICE_ACCOUNT_BQ_ADMIN)
# define the cloud storage connector. Allowing to communicate data
# between tasks
cloud_storage_conn = CloudStorageConnector("airflow_task_communication",
                                           settings.SERVICE_ACCOUNT_STORAGE_ADMIN)


def get_task_group_from_source(
    source_connector, dag: DAG, op_kwargs_extract: dict
) -> TaskGroup:
    """
    Creates a TaskGroup that contains two tasks, 'extract' and 'load', for
    each data_entity to be fetched from the specified source of the connector
    and loaded into BigQuery.

    :param source_connector: The connector object responsible for fetching
    data. The connector is assosiated to a specific source (mongodb, s3...).
    These are objects inherited from the BaseApiConnector class.

    :param dag: The DAG to which the tasks will be associated.

    :param op_kwargs_extract: Additional keyword arguments passed to the
    extract_data function (typically, parameters required for data extraction,
    filters for example).

    :param op_kwargs_load: Additional keyword arguments passed to the
    load_data function of the bigquery connector (typically, parameters
    used to define duplicates removal rules).

    :return: A TaskGroup object that encapsulates the extract and load tasks
    for each data entity of the connector source.
    """
    task_groupe_name = source_connector.name + "_to_bq"
    # Get data entities names to fetch from the source
    data_entities = get_data_types_to_fetch(
        source_connector.name, source_connector.database
    )

    # Build task group
    with TaskGroup(task_groupe_name) as task_group:
        for data_entity in list(data_entities.keys()):
            # Getting the coresponding BQ schema
            schema = load_schema(data_entity)

            # Extract Task
            # building op_kwargs for extract task
            op_kwargs_et = {
                **{"data_entity": data_entity, "save_res_to_s3": True},
                **op_kwargs_extract,
            }
            extract_task = PythonOperator(
                task_id=f"extract_{data_entity}",
                python_callable=source_connector.fetch_data,
                op_kwargs=op_kwargs_et,
                provide_context=True,
                dag=dag,
            )

            # Load Task
            # building op_kwargs for load task
            op_kwargs_lt = {
                "data": None,
                "data_entity": data_entity,
                "schema": schema,
                "duplicate_columns": data_entities[data_entity]["duplicate_columns"],
                "order_columns": data_entities[data_entity]["order_columns"]
            }
            load_task = PythonOperator(
                task_id=f"load_{data_entity}",
                python_callable=bigquery_conn.insert_data,
                op_kwargs=op_kwargs_lt,
                provide_context=True,
                dag=dag,
            )

            # Setting taks dependencies
            extract_task >> load_task

    return task_group
