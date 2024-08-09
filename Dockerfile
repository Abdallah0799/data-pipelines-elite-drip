FROM apache/airflow:2.9.3

# Install pipenv
RUN pip install pipenv

# Copy your custom DAGs or plugins
COPY dags/ /opt/airflow/dags/


# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install dependencies from Pipfile
RUN pipenv install
