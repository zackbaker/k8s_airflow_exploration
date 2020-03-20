from airflow import DAG
from datetime import timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': '2020-03-20 10:00:00',
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'dag_example',
    default_args=default_args,
    schedule_interval=timedelta(minutes=10),
    max_active_runs=1,
)

count = KubernetesPodOperator(
    namespace='airflow',
    image="zackbaker/k8s_airflow_test:latest",
    cmds=["python", "dag_example/tasks/count.py"],
    name="counting",
    task_id="counting",
    in_cluster=True,
    get_logs=True,
    dag=dag
)

coin_flip = KubernetesPodOperator(
    namespace='airflow',
    image="zackbaker/k8s_airflow_test:latest",
    cmds=["python", "dag_example/tasks/coin_flip.py"],
    name="coin-flip",
    task_id="coin-flip",
    in_cluster=True,
    get_logs=True,
    dag=dag
)

finished = KubernetesPodOperator(
    namespace='airflow',
    image="zackbaker/k8s_airflow_test:latest",
    cmds=["python", "dag_example/tasks/finished.py"],
    name="finished",
    task_id="finished",
    in_cluster=True,
    get_logs=True,
    dag=dag
)

finished.set_upstream([count, coin_flip])
