from airflow import DAG 
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta
import os 
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../etls')))

from steam_etl import extract_and_transform,load_data_to_csv
# Maybe implement TaskFlow instead. It looks easier to read.

default_args = {
    'owner': 'Jordan Welborn',
    'start_date': datetime(year=2024,month=10,day=20),
    'retries': 1
}

dag = DAG(
    dag_id= 'etl_steam_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['steam', 'etl', 'pipeline']
)

# extract from steam NEED to know what parameters need to pass into the pipeline
extract_transform = PythonOperator(
    task_id = 'steam_extraction',
    python_callable = extract_and_transform,
    execution_timeout=timedelta(seconds=60),
    op_kwargs = {
        'limit': 10000
    },
    dag=dag
)
load = PythonOperator(
    task_id = 'steam_load',
    python_callable = load_data_to_csv,
    execution_timeout=timedelta(seconds=60),
    op_kwargs={'games_df': '{{ task_instance.xcom_pull(task_ids="extract_and_transform") }}'},
    dag=dag
)