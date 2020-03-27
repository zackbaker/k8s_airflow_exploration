from airflow import DAG
from datetime import timedelta, datetime

from airflow.contrib.kubernetes.volume import Volume
from airflow.contrib.kubernetes.volume_mount import VolumeMount
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator


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
    'random_number_generator',
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
    read_only=False
)

timestamp = datetime.now()

create_file = KubernetesPodOperator(
    namespace='airflow',
    image="debian:9.4",
    cmds=["bash", "-c"],
    arguments=['echo $(($RANDOM%10000+10000)) >> /mnt/file-store/random_number-' + str(timestamp) + '.txt'],
    name="generate-random-number",
    task_id="generate-random-number",
    volumes=[volume],
    volume_mounts=[volume_mount],
    in_cluster=True,
    get_logs=True,
    dag=dag
)
