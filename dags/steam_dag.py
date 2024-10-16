from airflow import DAG, PythonOperator, LambdaCreateFunctionOperator
from datetime import datetime
import os 
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

default_args = {
    'owner': 'Jordan Welborn',
    'start_date': datetime(year: 2024,month:10,day:13)
    'retries': 3,
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

# Got a list of game ids
#TODO: Store this in a s3 bucket. First need the bucket name and dir im putting it in. 
def get_game_ids():
    url = 'http://api.steampowered.com/ISteamApps/GetAppList/v2/'
    response = requests.get(url)
    app_list = response.json()
    app_list = app_list['applist']['apps']
    list = []
    for app in app_list:
        appid = app['appid']
        list.append(appid)
    
        


get_id = PythonOperator(
    task_id='get_ids',
    python_callable=get_game_ids,
    dag=dag
)
# first we need all the game ids. 
# and store them in a s3 bucket because it is a large dataset.

# second we go through each game id and invoke the lambda function and pass in the payload

# Then we create another task called transform task which transforms that data into bronze data and dumps it in s3

# Then in the bronze data in s3 we can transform it once again with necessary changes to make the silver data. Maybe do all that in AWS IDK.

# invoking the lambda function to run
invoke_lambda_function= LambdaInvokeFunctionOperator(
    task_id = "invoke_lambda_function",
    function_name = steam_extract,
    payload=json.dumps({"SampleEvent": {"SampleData": {"Name": "XYZ", "DoB": "1993-01-01"}}}),
    log_type = 'Tail', 
    aws_conn_id='aws_default',
    dag=dag
)
# upload to s3 bucket.