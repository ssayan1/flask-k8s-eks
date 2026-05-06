# Two-Tier Flask App on AWS EKS

<div align="center">

![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-EKS-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-20.10+-2496ED?style=for-the-badge&logo=docker&logoColor=white)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen?style=flat-square)
![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=flat-square)

A **production-grade, cloud-native two-tier web application** deployed on Kubernetes (AWS EKS) with MySQL database, auto-scaling, and enterprise-ready infrastructure.

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Deployment](#installation--deployment)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Features](#features)
- [Troubleshooting](#troubleshooting)
- [Cost Optimization](#cost-optimization)
- [License](#license)

---

## 🎯 Overview

This project demonstrates **modern DevOps and cloud-native architecture** best practices by deploying a scalable Flask REST API with a persistent MySQL database on AWS EKS. It showcases containerization, Kubernetes orchestration, infrastructure automation, and production-ready patterns.

**Perfect for**: Portfolio projects, microservices learning, cloud architecture demonstrations, or production deployments.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│              AWS EKS Cluster (us-east-1)                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────┐        ┌──────────────────────┐  │
│  │   Flask API      │        │   MySQL Database     │  │
│  │  (Deployment)    │◄──────►│   (StatefulSet)      │  │
│  │  2–5 Replicas    │        │   with PVC (5Gi)     │  │
│  │  (Auto-scaled)   │        │   (EBS Backed)       │  │
│  └──────────────────┘        └──────────────────────┘  │
│         ▲                             ▲                 │
│         │                             │                 │
│  ┌──────┴─────────────────────────────┴─────┐          │
│  │   AWS Application Load Balancer           │          │
│  │   (Public Endpoint)                       │          │
│  └───────────────────────────────────────────┘          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Key Components:

- **Frontend/Backend**: Flask (Python) REST API
- **Database**: MySQL 8.0 (StatefulSet with persistent storage)
- **Cloud Platform**: AWS EKS (Elastic Kubernetes Service)
- **Storage**: AWS EBS via PersistentVolumeClaim (5Gi)
- **Scaling**: Horizontal Pod Autoscaler (2–5 replicas at 60% CPU)
- **Registry**: Amazon ECR
- **Load Balancing**: AWS Application Load Balancer

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Container Runtime** | Docker | 20.10+ |
| **Orchestration** | Kubernetes | 1.27+ |
| **Cloud Provider** | AWS (EKS) | Latest |
| **Application** | Flask | 2.0+ |
| **Language** | Python | 3.11 |
| **Database** | MySQL | 8.0 |
| **Package Manager** | pip | Latest |
| **IaC Tool** | eksctl | Latest |

---

## 📁 Project Structure

```
flask-k8s/
├── app/                          # Application code
│   ├── app.py                   # Flask REST API
│   ├── requirements.txt         # Python dependencies
│   └── Dockerfile               # Docker image definition
│
├── k8s/                         # Kubernetes manifests
│   ├── mysql-secret.yaml        # Database credentials (K8s Secret)
│   ├── mysql-pvc.yaml           # EBS persistent volume claim
│   ├── mysql-statefulset.yaml   # MySQL StatefulSet + Service
│   ├── flask-deployment.yaml    # Flask deployment + LoadBalancer
│   └── flask-hpa.yaml           # Horizontal Pod Autoscaler policy
│
└── README.md                    # This file
```

---

## 📋 Prerequisites

Before deploying, ensure you have:

### **Local Tools**
- ✅ `eksctl` (v0.180+) - EKS cluster management
- ✅ `kubectl` (v1.27+) - Kubernetes CLI
- ✅ `docker` (v20.10+) - Container runtime
- ✅ `aws-cli` (v2.13+) - AWS command line
- ✅ Python 3.11+ (for local testing)

### **AWS Setup**
- ✅ AWS account with active credentials
- ✅ IAM permissions for EC2, EKS, VPC, EBS
- ✅ AWS CLI configured (`aws configure`)
- ✅ ECR repository created (optional, for custom images)

### **Installation**

```bash
# macOS (using Homebrew)
brew install eksctl kubectl docker awscli

# Ubuntu/Debian
sudo apt-get install docker.io
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# Windows (using Chocolatey)
choco install eksctl kubectl docker awscli
```

---

## 🚀 Installation & Deployment

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/yourusername/flask-k8s.git
cd flask-k8s
```

### **Step 2: Create AWS EKS Cluster**
```bash
eksctl create cluster \
  --name flask-mysql-cluster \
  --region us-east-1 \
  --node-type t3.medium \
  --nodes 2 \
  --managed
```
⏱️ *This takes ~15-20 minutes. Grab a coffee!*

### **Step 3: Verify Cluster Access**
```bash
# Test kubectl connection
kubectl get nodes
kubectl get pods -A
```

### **Step 4: Build & Push Docker Image (Optional)**
```bash
# Build Docker image locally
docker build -t flask-k8s:1.0.0 app/

# Tag for ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
docker tag flask-k8s:1.0.0 <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/flask-k8s:1.0.0
docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/flask-k8s:1.0.0
```

### **Step 5: Create Namespace & Secrets**
```bash
# Create application namespace
kubectl create namespace flask-app

# Create MySQL secret (update credentials!)
kubectl create secret generic mysql-secret \
  --from-literal=MYSQL_ROOT_PASSWORD=your_secure_password \
  --from-literal=MYSQL_USER=flask_user \
  --from-literal=MYSQL_PASSWORD=your_flask_password \
  --from-literal=MYSQL_DB=flask_db \
  -n flask-app
```

### **Step 6: Deploy to Kubernetes**
```bash
# Apply all manifests
kubectl apply -f k8s/ -n flask-app

# Verify deployment
kubectl get all -n flask-app
kubectl logs -f deployment/flask-app -n flask-app
```

### **Step 7: Get Load Balancer Endpoint**
```bash
kubectl get svc -n flask-app

# Wait for EXTERNAL-IP to be assigned (5-10 minutes)
# Then access: http://<EXTERNAL-IP>:5000
```

---

## 📡 API Documentation

### **Endpoints**

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| `GET` | `/` | Health check & MySQL version | `{"status": "ok", "mysql_version": "8.0.x"}` |

### **Example Requests**

```bash
# Health check
curl http://<LOAD_BALANCER_IP>:5000/

# Example response
{
  "status": "ok",
  "mysql_version": "8.0.32-0ubuntu0.22.04.1"
}
```

---

## ⚙️ Configuration

### **Environment Variables**

The Flask app requires the following environment variables (injected via Kubernetes Secrets):

| Variable | Description | Example |
|----------|-------------|---------|
| `MYSQL_HOST` | MySQL service hostname | `mysql-service.flask-app.svc.cluster.local` |
| `MYSQL_USER` | Database user | `flask_user` |
| `MYSQL_PASSWORD` | Database password | `secure_password` |
| `MYSQL_DB` | Database name | `flask_db` |

### **Scaling Configuration**

Edit `k8s/flask-hpa.yaml` to adjust autoscaling:

```yaml
spec:
  minReplicas: 2          # Minimum pod replicas
  maxReplicas: 5          # Maximum pod replicas
  targetCPUUtilizationPercentage: 60  # Scale trigger (%)
```

### **Storage Configuration**

Modify `k8s/mysql-pvc.yaml` to change storage size:

```yaml
resources:
  requests:
    storage: 5Gi   # Change this value
```

---

## ✨ Features

✅ **Kubernetes Native**
- StatefulSet for MySQL with persistent storage
- Deployment with rolling updates
- Service mesh-ready architecture

✅ **High Availability**
- Horizontal Pod Autoscaler (2-5 replicas)
- Readiness probes for zero-downtime deployments
- Resource requests and limits defined

✅ **Security**
- Kubernetes Secrets for credential management
- Network policies ready
- Container security best practices

✅ **Cloud Integration**
- AWS EBS for persistent storage
- AWS ALB for load balancing
- AWS ECR for image registry

✅ **Production Ready**
- Health checks and probes
- Resource constraints
- Proper logging and monitoring integration points

✅ **DevOps Best Practices**
- Infrastructure as Code (IaC)
- Container-based deployment
- Declarative configuration

---

## 🔧 Troubleshooting

### **Pod Not Starting?**
```bash
# Check pod logs
kubectl logs <pod-name> -n flask-app

# Describe pod for events
kubectl describe pod <pod-name> -n flask-app

# Common issues:
# - MySQL not ready: Wait for mysql-0 pod to be running
# - Image pull errors: Check ECR credentials
# - Memory/CPU issues: Increase node resources
```

### **Database Connection Error**
```bash
# Verify MySQL is running
kubectl get pods -n flask-app | grep mysql

# Check secrets exist
kubectl get secrets -n flask-app

# Test MySQL connectivity from Flask pod
kubectl exec -it <flask-pod> -n flask-app -- bash
mysql -h mysql-service -u flask_user -p
```

### **Load Balancer Not Getting IP**
```bash
# Wait up to 5 minutes for AWS to assign IP
kubectl get svc -n flask-app -w

# Check ALB controller logs
kubectl logs -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller
```

### **Persistent Volume Issues**
```bash
# Check PVC status
kubectl get pvc -n flask-app

# Describe PVC for details
kubectl describe pvc mysql-pvc -n flask-app
```

---

## 💰 Cost Optimization

### **Reduce AWS Costs**

```bash
# Use spot instances for non-critical workloads
eksctl create nodegroup \
  --cluster=flask-mysql-cluster \
  --spot \
  --instance-types=t3.medium

# Scale down during off-hours
kubectl scale deployment flask-app --replicas=1 -n flask-app

# Clean up unused resources
eksctl delete cluster --name flask-mysql-cluster
```

**Estimated Monthly Cost** (us-east-1):
- EKS Control Plane: $0.10/hour (~$73/month)
- 2x t3.medium EC2 nodes: ~$60/month
- EBS Storage (5Gi): ~$0.50/month
- **Total: ~$133/month**

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📬 Support & Feedback

- **Issues**: [GitHub Issues](https://github.com/yourusername/flask-k8s/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/flask-k8s/discussions)
- **Email**: your.email@example.com

---

<div align="center">

**Made with ❤️ for the DevOps & Cloud Community**

[![GitHub followers](https://img.shields.io/github/followers/yourusername?style=social)](https://github.com/yourusername)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/flask-k8s?style=social)](https://github.com/yourusername/flask-k8s)

</div>
