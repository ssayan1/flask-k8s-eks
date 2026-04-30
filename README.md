# Two-Tier Flask App on AWS EKS

A production-grade two-tier web application deployed on Kubernetes (AWS EKS).

## Architecture

- **Frontend/Backend**: Flask (Python) REST API
- **Database**: MySQL 8.0 (StatefulSet with persistent storage)
- **Cloud**: AWS EKS (Elastic Kubernetes Service)
- **Storage**: AWS EBS via PersistentVolumeClaim (5Gi)
- **Scaling**: Horizontal Pod Autoscaler (2–5 replicas at 60% CPU)
- **Registry**: Amazon ECR

## Project Structure
```
flask-k8s/
├── app/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Container image
└── k8s/
├── mysql-secret.yaml       # Credentials (Kubernetes Secret)
├── mysql-pvc.yaml          # Persistent storage (EBS)
├── mysql-statefulset.yaml  # MySQL StatefulSet + Service
├── flask-deployment.yaml   # Flask Deployment + LoadBalancer
└── flask-hpa.yaml          # Horizontal Pod Autoscaler
```
## Features

- Kubernetes Secrets for secure credential management
- EBS-backed PersistentVolumeClaim for MySQL data durability
- Readiness probes for zero-downtime deployments
- Resource requests and limits on all containers
- AWS Load Balancer for public traffic
- HPA autoscaling based on CPU utilization

## Deploy

```bash
# Create EKS cluster
eksctl create cluster --name flask-mysql-cluster --region us-east-1 --node-type t3.medium --nodes 2 --managed

# Apply manifests
kubectl create namespace flask-app
kubectl apply -f k8s/ -n flask-app
