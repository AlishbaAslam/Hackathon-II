---
name: deploy_to_minikube
description: Generate step-by-step, copy-paste-ready commands for deploying the Helm chart on Minikube, including verification, troubleshooting, and kagent analysis for Phase-IV Todo Chatbot. Never modifies code or specs – only generates safe deployment instructions.
---
# Deployment to Minikube Skill for Phase-IV

## Instructions
1. **Pre-deployment Checks**
   - Verify Minikube is running and healthy
   - Check kubectl context and nodes
   - Ensure Helm chart exists at phase-II-full-stack-todo/helm/todo-chart/

2. **Helm Deployment**
   - Run helm install or upgrade command
   - Use release name "todo-app"
   - Deploy in default namespace

3. **Verification & Access**
   - Check pods, services, ingress status
   - Get Minikube service URL for browser access
   - Run kagent analysis for cluster health

4. **Troubleshooting**
   - Common fixes for ImagePullBackOff, CrashLoopBackOff, etc.
   - kubectl describe/logs/events commands

## Best Practices
- Always check minikube status first
- Use helm upgrade --install for idempotent deployment
- Verify pods are Running before accessing
- Use kagent for intelligent cluster analysis
- Include dry-run or --debug flags when testing
- Provide clear access URL (minikube service --url)
- Add namespace if not default
- Clean up with helm uninstall if needed

## Example Structure

### Full Deployment Guide (example output)
```bash
# 1. Pre-checks
minikube status
kubectl get nodes

# 2. Helm install
helm upgrade --install todo-app ./helm/todo-chart --namespace default

# 3. Verification
kubectl get pods
kubectl get services
kubectl get ingress

# 4. Access app
minikube service todo-frontend --url

# 5. kagent analysis
kagent "analyze the cluster health"
kagent "check why pods are failing if any"
```

### Complete Deployment Script
```bash
#!/bin/bash

# Phase-IV: Deploy Todo Chatbot to Minikube
# Prerequisites: Minikube running, kubectl configured, Helm installed

set -e  # Exit on any error

echo "=== Pre-deployment Checks ==="
echo "Checking Minikube status..."
minikube status

echo "Verifying kubectl context..."
kubectl cluster-info

echo "Checking nodes..."
kubectl get nodes

echo "Verifying Helm installation..."
helm version

echo "Checking if Helm chart exists..."
if [ ! -d "./helm/todo-chart" ]; then
    echo "ERROR: Helm chart not found at ./helm/todo-chart"
    exit 1
fi

echo "=== Deploying Todo Chatbot ==="
echo "Installing/upgrading Helm release 'todo-app'..."

# Deploy the application
helm upgrade --install todo-app ./helm/todo-chart \
  --namespace default \
  --wait \
  --timeout=10m \
  --debug

echo "=== Verifying Deployment ==="
echo "Checking pods..."
kubectl get pods

echo "Checking services..."
kubectl get services

echo "Checking ingress..."
kubectl get ingress

echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=backend --timeout=300s
kubectl wait --for=condition=ready pod -l app=frontend --timeout=300s

echo "=== Access Information ==="
echo "Getting service URLs..."

echo "Frontend URL:"
minikube service todo-app-frontend --url

echo "Backend URL:"
minikube service todo-app-backend --url

echo "=== Health Checks ==="
echo "Checking application endpoints..."

FRONTEND_URL=$(minikube service todo-app-frontend --url --format "{{.URL}}")
BACKEND_URL=$(minikube service todo-app-backend --url --format "{{.URL}}")

echo "Frontend: $FRONTEND_URL"
echo "Backend: $BACKEND_URL"

echo "Testing backend health..."
curl -f "$BACKEND_URL/health" || echo "Backend health check failed"

echo "=== Cluster Analysis ==="
echo "Running kagent analysis..."
kagent "analyze the cluster health and report any issues"
kagent "check if there are any resource constraints or pod issues"

echo "=== Deployment Complete ==="
echo "Todo Chatbot deployed successfully!"
echo "Access the frontend at: $FRONTEND_URL"
echo "Access the backend at: $BACKEND_URL"
```

### Troubleshooting Commands
```bash
# Common troubleshooting commands

# Check pod status and logs
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name> -c <container-name>
kubectl logs <pod-name> -c <container-name> --previous

# Check service and ingress
kubectl get services
kubectl describe service <service-name>
kubectl get ingress
kubectl describe ingress <ingress-name>

# Check events for debugging
kubectl get events --sort-by='.lastTimestamp'

# Port forward for direct access (if service/ingress not working)
kubectl port-forward service/todo-app-frontend 3000:3000
kubectl port-forward service/todo-app-backend 8000:8000

# Check resource usage
kubectl top nodes
kubectl top pods

# Helm operations
helm list
helm status todo-app
helm rollback todo-app 1
helm uninstall todo-app

# Minikube specific
minikube dashboard
minikube tunnel  # For LoadBalancer services
minikube addons list
minikube addons enable ingress  # Enable ingress if not enabled
```

### Cleanup Commands
```bash
# Cleanup commands

# Uninstall the Helm release
helm uninstall todo-app

# Delete all resources manually (if needed)
kubectl delete pods,services,deployments,ingress -l app=backend
kubectl delete pods,services,deployments,ingress -l app=frontend

# Reset Minikube (nuclear option)
minikube delete
minikube start
minikube addons enable ingress
```

### Dry Run and Debug Commands
```bash
# Test deployment without applying
helm install todo-app ./helm/todo-chart --dry-run --debug

# Template validation
helm template todo-app ./helm/todo-chart

# Validate with kubeval (if installed)
helm template todo-app ./helm/todo-chart | kubeval

# Deploy with specific values
helm upgrade --install todo-app ./helm/todo-chart \
  --set backend.replicaCount=2 \
  --set frontend.replicaCount=2
```