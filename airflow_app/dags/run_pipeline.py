from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG

from dbt_airflow.core.config import DbtAirflowConfig, DbtProjectConfig, DbtProfileConfig
from dbt_airflow.core.task_group import DbtTaskGroup
from dbt_airflow.core.task import ExtraTask
from dbt_airflow.operators.execution import ExecutionOperator

from data_engineering.airflow_utils.extract_load_task_group import (
    get_task_group_from_source,
)

import settings

# Import all connectors from source we want to extract
from data_engineering.api_connectors.mongodb import MongoDbConnector
from data_engineering.api_connectors.s3 import S3Connector
from data_engineering.api_connectors.balldontlie import BallDontLie


# Build the dag
with DAG(
    dag_id="data_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@hourly",
    catchup=False,
    tags=["business"],
    default_args={
        "owner": "airflow",
        "retries": 0,
        "retry_delay": timedelta(minutes=1),
    },
    dagrun_timeout=timedelta(minutes=50),
) as dag:

    # Define the required connectors
    mongo_db_database = "center"
    s3_database = "fictive-company"
    balldontlie_database = "nba"

    mongo_db_connector = MongoDbConnector(mongo_db_database)
    s3_connector = S3Connector(s3_database)
    balldontlie_connector = BallDontLie(balldontlie_database)

    # Build the required task groups
    mongodb_to_bq = get_task_group_from_source(
        mongo_db_connector,
        dag,
        {
            "filters": {
                "updated_at": {
                    "$gte": (datetime.now() - timedelta(settings.MONGO_DB_FETCH_WINDOW))
                }
            }
        },
    )

    s3_to_bq = get_task_group_from_source(
        s3_connector, dag, {"datetime_window_filter": settings.S3_FETCH_WINDOW}
    )

    bdl_to_bq = get_task_group_from_source(
        balldontlie_connector, dag, {"params": {"per_page": 100}}
    )

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

    mongodb_to_bq >> s3_to_bq >> bdl_to_bq >> dbt_run
