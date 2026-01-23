# Phase-IV: Local Kubernetes Deployment of Todo Chatbot on Minikube with Helm Charts

This directory contains all the artifacts needed to deploy the Todo Chatbot application on a local Kubernetes cluster using Minikube and Helm charts.

## Overview

This project demonstrates cloud-native deployment capabilities by containerizing the Todo Chatbot application (from Phase-III) and deploying it to a local Kubernetes cluster. The solution includes:

- Optimized Docker images for both backend (FastAPI) and frontend (Next.js) components
- Comprehensive Helm chart for unified deployment
- Integration with AI-assisted Kubernetes tools (kubectl-ai/kagent)
- Resource-efficient configuration suitable for development environments

## Architecture

```
┌─────────────────┐    ┌──────────────────────┐
│   Developer     │    │                      │
│   Workstation   │    │   Minikube Cluster   │
│                 │    │                      │
│  ┌───────────┐  │    │  ┌─────────────────┐ │
│  │Helm CLI   │  │    │  │  Backend Pod    │ │
│  │           │  │────┼──▶│(FastAPI App)    │ │
│  └───────────┘  │    │  └─────────────────┘ │
│                 │    │                      │
│  ┌───────────┐  │    │  ┌─────────────────┐ │
│  │Docker CLI │  │────┼──▶│  Frontend Pod   │ │
│  │           │  │    │  │(Next.js App)    │ │
│  └───────────┘  │    │  └─────────────────┘ │
└─────────────────┘    │                      │
                       │  ┌─────────────────┐ │
                       │  │  Service/Ingress│ │
                       │  │  (Load Balancer)│ │
                       │  └─────────────────┘ │
                       └──────────────────────┘
```

## Prerequisites

- Docker Desktop or Docker Engine
- Minikube (v1.30+)
- Helm (v3.10+)
- kubectl (v1.25+)
- At least 4GB free RAM and 10GB disk space

## Deployment Instructions

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

## Project Structure

```
phase-IV-k8s-deployment/
├── docker/
│   ├── Dockerfile.backend    # Multi-stage build for FastAPI backend
│   ├── Dockerfile.frontend   # Multi-stage build for Next.js frontend
│   └── .dockerignore         # Files to exclude from Docker build context
├── helm/
│   └── todo-chart/           # Helm chart for Todo Chatbot
│       ├── Chart.yaml        # Chart metadata
│       ├── values.yaml       # Default configuration values
│       ├── templates/
│       │   ├── deployment-backend.yaml    # Backend deployment manifest
│       │   ├── deployment-frontend.yaml   # Frontend deployment manifest
│       │   ├── service-backend.yaml       # Backend service manifest
│       │   ├── service-frontend.yaml      # Frontend service manifest
│       │   ├── ingress.yaml              # Ingress controller manifest
│       │   └── configmap.yaml            # Application configuration
│       └── README.md           # Chart documentation
└── README.md                 # Overall deployment instructions
```

## Quality Assurance

- Docker images optimized to stay under 500MB each
- Resource limits configured for development environment constraints
- Health checks implemented for both services
- Proper isolation maintained (Phase-II-full-stack-todo remains unmodified)