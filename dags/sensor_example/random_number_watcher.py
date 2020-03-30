from airflow import DAG
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
    'retries': 0
}

dag = DAG(
    'random_number_watcher',
    default_args=default_args,
    schedule_interval='*/1 * * * *',
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


check_for_file = KubernetesPodOperator(
    namespace='airflow',
    task_id='check-for-file',
    name='check-for-file',
    volumes=[volume],
    volume_mounts=[volume_mount],
    image='zackbaker/k8s_airflow_test:latest',
    cmds=["python", "dags/sensor_example/tasks/file_creation_watcher.py"],
    # xcom_push=True,
    in_cluster=True,
    get_logs=True,
    dag=dag
)
