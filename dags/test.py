from airflow import DAG
from datetime import timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': '2020-03-20 09:00:00',
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'kubernetes_sample',
    default_args=default_args,
    schedule_interval=timedelta(minutes=10),
)

start = DummyOperator(task_id='run_this_first', dag=dag)

passing = KubernetesPodOperator(
    namespace='airflow',
    image="python:3.7",
    cmds=["python", "-c"],
    arguments=["print('hello world')"],
    labels={"foo": "bar"},
    name="passing-test",
    task_id="passing-task",
    in_cluster=True,
    get_logs=True,
    dag=dag
)

failing = KubernetesPodOperator(
    namespace='airflow',
    image="ubuntu:16.04",
    cmds=["python", "-c"],
    arguments=["print('hello world')"],
    labels={"foo": "bar"},
    name="fail",
    task_id="failing-task",
    in_cluster=True,
    get_logs=True,
    dag=dag
)

passing.set_upstream(start)
failing.set_upstream(start)
