from dags.sensor_example.tasks import check_for_file

from airflow import DAG
from datetime import timedelta, datetime
from airflow.contrib.kubernetes.volume import Volume
from airflow.contrib.kubernetes.volume_mount import VolumeMount
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': '2020-03-20 09:00:00',
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'random_number_watcher',
    default_args=default_args,
    schedule_interval='*/5 * * * *',
    catchup=False
)

volume_config = {
    'persistentVolumeClaim': {
        'claimName': 'file-store'
    }
}
volume = Volume(name='file-store', configs=volume_config)
volume_mount = VolumeMount(
    'file-store',
    mount_path='/mnt/file-store',
    sub_path=None,
    read_only=False
)

run_this = PythonOperator(
    task_id='python_operator',
    provide_context=True,
    python_callable=check_for_file.run,
    dag=dag
)


# create_file = KubernetesPodOperator(
#     namespace='airflow',
#     image="zackbaker/k8s_airflow_test:latest",
#     cmds=["python", "sensor_example/tasks/check_for_file.py"],
#     name="random-number-notifier",
#     task_id="random-number-notifier",
#     volumes=[volume],
#     volume_mounts=[volume_mount],
#     in_cluster=True,
#     get_logs=True,
#     dag=dag
# )