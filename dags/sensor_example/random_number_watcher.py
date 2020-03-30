from airflow import DAG
from airflow.contrib.kubernetes.volume import Volume
from airflow.contrib.kubernetes.volume_mount import VolumeMount
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.bash_operator import BashOperator

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

bash_op = BashOperator(
     task_id='bash_task',
     bash_command='echo "Here is the message: '
                  '{{ dag_run.conf["file_path"] if dag_run else "" }}"',
     dag=dag,
)

# check_for_file = KubernetesPodOperator(
#     namespace='airflow',
#     task_id='check-for-file',
#     name='check-for-file',
#     volumes=[volume],
#     volume_mounts=[volume_mount],
#     image='zackbaker/k8s_airflow_test:latest',
#     cmds=["python", "dags/sensor_example/tasks/print_number.py"],
#     xcom_push=True,
#     in_cluster=True,
#     get_logs=True,
#     dag=dag
# )
