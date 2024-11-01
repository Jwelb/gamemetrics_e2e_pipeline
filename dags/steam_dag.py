from airflow import DAG 
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta
import os 
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../pipeline')))

from game_pipeline import game_pipeline
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
    schedule_interval='@Weekly',
    catchup=False,
    tags=['data', 'etl', 'pipeline']
)

# Break out each task of the pipeline [DONE]
# Make one big extraction file and one big load file
# Change the task id to reflect the API were using [DONE]
extract_transform = PythonOperator(
    task_id = 'game_extraction',
    python_callable = game_pipeline,
    execution_timeout=timedelta(minutes=30),
    op_kwargs = {
        'limit': 10000
    },
    dag=dag
)
load = PythonOperator(
    task_id = 'steam_load',
    python_callable = load_data_to_csv,
    execution_timeout=timedelta(seconds=60),
    op_kwargs={'games_df': '{{ task_instance.xcom_pull(task_ids="game_extraction") }}'},
    dag=dag
)