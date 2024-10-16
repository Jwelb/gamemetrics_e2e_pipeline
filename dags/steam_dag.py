from airflow import DAG 
from airflow.operators.python import PythonOperator
from datetime import datetime
import os 
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../pipelines')))

from steam_pipeline import steam_pipeline
# Maybe implement TaskFlow instead. It looks easier to read.

default_args = {
    'owner': 'Jordan Welborn',
    'start_date': datetime(year=2024,month=10,day=13),
    'retries': 3
}

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
        'limit': 10000
    },
    dag=dag
)
# first we need all the game ids. 
# and store them in a s3 bucket because it is a large dataset.

# second we go through each game id and invoke the lambda function and pass in the payload

# Then we create another task called transform task which transforms that data into bronze data and dumps it in s3

# Then in the bronze data in s3 we can transform it once again with necessary changes to make the silver data. Maybe do all that in AWS IDK.

# invoking the lambda function to run
# upload to s3 bucket.