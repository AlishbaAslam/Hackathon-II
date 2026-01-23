# Quickstart Guide: Phase-IV Kubernetes Deployment

## Prerequisites

- Docker Desktop or Docker Engine
- Minikube (v1.30+)
- Helm (v3.10+)
- kubectl (v1.25+)
- At least 4GB free RAM and 10GB disk space

## Quick Setup

### 1. Start Minikube

```bash
# Start Minikube with Docker driver and specified resources
minikube start --driver=docker --cpus=2 --memory=2gb --disk-size=10g

# Enable ingress addon
minikube addons enable ingress

# Verify cluster is running
kubectl cluster-info
```

### 2. Build Docker Images

```bash
# Point Docker CLI to Minikube's Docker daemon
eval $(minikube docker-env)

# Build backend image
cd /path/to/repo
docker build -f phase-IV-k8s-deployment/docker/Dockerfile.backend -t todo-backend:latest .

# Build frontend image
docker build -f phase-IV-k8s-deployment/docker/Dockerfile.frontend -t todo-frontend:latest .
```

### 3. Install Helm Chart

```bash
# Navigate to the Helm chart directory
cd phase-IV-k8s-deployment/helm/todo-chart

# Install the chart
helm install todo-chatbot . --values values.yaml
```

### 4. Verify Deployment

```bash
# Check if pods are running
kubectl get pods

# Check services
kubectl get services

# Access the application
minikube service todo-frontend-svc --url
```

## Troubleshooting

### Common Issues

1. **Minikube won't start**
   ```bash
   # Stop and delete any existing cluster
   minikube delete
   # Start with explicit resources
   minikube start --driver=docker --cpus=2 --memory=2gb --disk-size=10g
   ```

2. **Images not found**
   ```bash
   # Make sure to run this before building images
   eval $(minikube docker-env)
   ```

3. **Ingress not working**
   ```bash
   # Verify ingress addon is enabled
   minikube addons list | grep ingress
   # Enable if disabled
   minikube addons enable ingress
   ```

### Cleanup

```bash
# Uninstall the Helm release
helm uninstall todo-chatbot

# Stop Minikube
minikube stop

# Optionally delete the cluster
minikube delete
```

## AI-Assisted Kubernetes Operations

The deployment includes integration with kubectl-ai and kagent for enhanced operations:

```bash
# Analyze cluster health
kubectl-ai "analyze the health of all pods in the default namespace"

# Troubleshoot deployment issues
kubectl-ai "show me pods that are not running and why"

# Get recommendations
kagent "analyze the todo-chatbot deployment and suggest optimizations"
```