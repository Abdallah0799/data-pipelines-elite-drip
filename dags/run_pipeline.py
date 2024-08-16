from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

from dbt_airflow.core.config import DbtAirflowConfig, DbtProjectConfig, DbtProfileConfig
from dbt_airflow.core.task_group import DbtTaskGroup
from dbt_airflow.core.task import ExtraTask
from dbt_airflow.operators.execution import ExecutionOperator
from dbt_airflow.operators.bash import DbtRunBashOperator

from data_engineering.actions import get_pipeline_task_group

import settings

# Import all connectors from source we want to extract
from data_engineering.api_connectors.mongodb import MongoDbConnector
from data_engineering.api_connectors.s3 import S3Connector

# Define the required connectors
mongo_db_database = "center"
s3_database = "fictive-company"

mongo_db_connector = MongoDbConnector(mongo_db_database)
s3_connector = S3Connector(s3_database)

# Build the dag
with DAG(
    dag_id="test_dag",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["example"],
    default_args={
        "owner": "airflow",
        "retries": 0,
        "retry_delay": timedelta(minutes=2),
    },
) as dag:

    # Build the required task groups
    mongodb_to_bq = get_pipeline_task_group(
        mongo_db_connector,
        dag,
        {
            #"filters": {
            #    "updated_at": {
            #        "$gte": (datetime.now() - timedelta(settings.MONGO_DB_FETCH_WINDOW))
            #    }
            #}
        },
    )

    s3_to_bq = get_pipeline_task_group(s3_connector,
                                       dag,
                                       {
                                           "datetime_window_filter": settings.S3_FETCH_WINDOW
                                       })

    dbt_run = DbtTaskGroup(
        group_id="dbt-bigquery-warehouse",
        dbt_project_config=DbtProjectConfig(
            project_path=Path("/opt/airflow/dbt/"),
            manifest_path=Path("/opt/airflow/dbt/target/manifest.json"),
        ),
        dbt_profile_config=DbtProfileConfig(
            profiles_path=Path("/opt/airflow/dbt/profiles"),
            target="dev",
        ),
        dbt_airflow_config=DbtAirflowConfig(
            execution_operator=ExecutionOperator.BASH,
        ),
    )

    [mongodb_to_bq, s3_to_bq] >> dbt_run
