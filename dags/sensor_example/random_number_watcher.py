from airflow import DAG
from airflow.contrib.kubernetes.volume import Volume
from airflow.contrib.kubernetes.volume_mount import VolumeMount
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.models.dagrun import DagRun

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
    dag_id='random_number_watcher',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
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

print_number = KubernetesPodOperator(
    namespace='airflow',
    task_id='print-number',
    name='print-number',
    volumes=[volume],
    volume_mounts=[volume_mount],
    image='zackbaker/k8s_airflow_test:latest',
    cmds=["python", "dags/sensor_example/tasks/print_number.py"],
    arguments=['{{ dag_run.conf["file_path"] }}'],
    in_cluster=True,
    get_logs=True,
    dag=dag
)

delete_file = KubernetesPodOperator(
    namespace='airflow',
    task_id='print-number',
    name='print-number',
    volumes=[volume],
    volume_mounts=[volume_mount],
    image='zackbaker/k8s_airflow_test:latest',
    cmds=["python", "dags/sensor_example/tasks/delete_file.py"],
    arguments=['{{ dag_run.conf["file_path"] }}'],
    in_cluster=True,
    get_logs=True,
    dag=dag
)
delete_file.set_upstream(print_number)
