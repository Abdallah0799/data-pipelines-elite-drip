FROM apache/airflow:2.9.3

# Install pipenv
RUN pip install pipenv

USER airflow

# Copy your custom DAGs or plugins
COPY --chown=airflow dags/ /opt/airflow/dags/

# Copy dbt folder
COPY --chown=airflow dbt/ /opt/airflow/dbt

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY --chown=airflow . ./

ENV PYTHONPATH /app

# Install dependencies from Pipfile
RUN pipenv install

# Save BQ KEY to folder
RUN pipenv run python utils/bq_service_account.py