# k8s_airflow_exploration
Exploring Airflow on k8s

## Setup Steps
- Download Docker and turn on Kubernetes
- Run the following commands
```bash
brew install helm
kubectl create namespace airflow
kubectl config set-context dev --namespace=airflow
helm install airflow stable/airflow -n airflow -f charts/values.yaml
```
- Next lets run port-forwarding in a screen
```bash
# Get our pod to forward
export POD_NAME=$(kubectl get pods --namespace airflow -l "component=web,app=airflow" -o jsonpath="{.items[0].metadata.name}")
# Forward the pod to 8080
screen kubectl port-forward --namespace airflow $POD_NAME 8080:8080
```
- - Then press ctrl+a d
- [Now go here](http://localhost:8080/admin/)