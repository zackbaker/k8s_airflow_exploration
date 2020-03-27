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


check_for_file = OmegaFileSensor(
    task_id='check_for_file',
    filepath='/mnt/file-store',
    filepattern='random',
    poke_interval=3,
    dag=dag
)
