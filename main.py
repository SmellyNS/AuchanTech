"""
DAG AIRFLOW
"""

import reader
import readerhard
import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'admin',
    'start_date': days_ago(0),
    'depends_on_past': False,
}


def getTestAuchanExample() -> None:
    reader.main()


def getTestAuchanExampleHard() -> None:
    readerhard.main()


with DAG(
        dag_id='AuchanTestReader',
        default_args=default_args,
        schedule_interval='@once',
        catchup=False
) as dag:
    start = EmptyOperator(
        task_id='start',
    )

    test_auchan_example_simple = PythonOperator(
        task_id='TestAuchanExampleSimple',
        python_callable=getTestAuchanExample,
    )
    test_auchan_example_hard = PythonOperator(
        task_id='TestAuchanExampleHard',
        python_callable=getTestAuchanExampleHard,
    )

    end = EmptyOperator(
        task_id='end',
    )

    ## Çàêîììåíòèğîâàí ãğàô ñ óïğîù¸ííûì ğåøåíèåì
    #start >> test_auchan_example_simple >> end
    start >> test_auchan_example_hard >> end
