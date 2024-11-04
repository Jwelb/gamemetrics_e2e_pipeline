from airflow import DAG 
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta
import os 
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../pipelines')))

from game_pipeline import extract_data,load_data
# Implement Task Flow Later refer to https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflow.html

default_args = {
    'owner': 'Jordan Welborn',
    'start_date': datetime(year=2024,month=11,day=1),
    'retries': 1
}
# This does not need to be daily it needs to be weekly [DONE]
# Change the dag id to reflect the API were using [Done]
dag = DAG(
    dag_id= 'etl_game_pipeline',
    default_args=default_args,
    schedule_interval='@weekly',
    catchup=False,
    tags=['data', 'etl', 'pipeline']
)

# Break out each task of the pipeline [DONE]
# Make one big extraction file and one big load file
# Change the task id to reflect the API were using [DONE]
extract= PythonOperator(
    task_id = 'game_extraction',
    python_callable = extract_data,
    execution_timeout=timedelta(minutes=30),
    op_kwargs = {
        'limit': 10000
    },
    dag=dag
)
load = PythonOperator(
    task_id = 'steam_load',
    python_callable = load_data,
    execution_timeout=timedelta(seconds=60),
    dag=dag
)