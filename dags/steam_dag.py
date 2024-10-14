from airflow import DAG, PythonOperator
from datetime import datetime
import os 
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

default_args = {
    'owner': 'Jordan Welborn',
    'start_date': datetime(year: 2024,month:10,day:13)
}

file_postfix = datetime.now().strftime("%Y%m%d")

dag = DAG(
    dag_id= 'etl_steam_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['steam', 'etl', 'pipeline']
)

# extract from steam NEED to know what parameters need to pass into the pipeline
extract = PythonOperator(
    task_id = 'steam_extraction',
    python_callable = steam_pipeline,
    op_kwargs = {
        'file_name': f'steam_{file_postfix}',
        'limit': 10000
    },
    dag=dag
)
# upload to s3 bucket.