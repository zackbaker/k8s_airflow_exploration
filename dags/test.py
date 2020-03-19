from airflow import DAG
from datetime import datetime, timedelta
# from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

if __name__ == '__main__':
    default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime.utcnow(),
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5)
    }

    dag = DAG(
        'kubernetes_sample',
        default_args=default_args,
        schedule_interval=timedelta(minutes=10)
    )

    start = DummyOperator(task_id='run_this_first', dag=dag)

    passing = BashOperator(
        task_id='passing',
        bash_command='echo Passing!'
    )

    failing = BashOperator(
        task_id='failing',
        bash_command='echo failing!; exit(1)'
    )

    # passing = KubernetesPodOperator(
    #     namespace='default',
    #     image="Python:3.6",
    #     cmds=["Python", "-c"],
    #     arguments=["print('hello world')"],
    #     labels={"foo": "bar"},
    #     name="passing-test",
    #     task_id="passing-task",
    #     get_logs=True,
    #     dag=dag
    # )
    #
    # failing = KubernetesPodOperator(
    #     namespace='default',
    #     image="ubuntu:1604",
    #     cmds=["Python", "-c"],
    #     arguments=["print('hello world')"],
    #     labels={"foo": "bar"},
    #     name="fail",
    #     task_id="failing-task",
    #     get_logs=True,
    #     dag=dag
    # )

    passing.set_upstream(start)
    failing.set_upstream(start)