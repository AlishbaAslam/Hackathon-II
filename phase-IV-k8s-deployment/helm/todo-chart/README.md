# Todo Chatbot Helm Chart

A Helm chart for deploying the Todo Chatbot application on Kubernetes. This chart deploys both the backend (FastAPI) and frontend (Next.js) components with appropriate services and ingress configuration.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.2+
- PV provisioner support in the underlying infrastructure (optional)

## Installing the Chart

To install the chart with the release name `todo-chatbot`:

```bash
# Add the chart repository if needed
helm repo add todo-chatbot https://github.com/AlishbaAslam/Hackathon-II

# Install the chart
helm install todo-chatbot . --values values.yaml
```

## Uninstalling the Chart

To uninstall/delete the `todo-chatbot` deployment:

```bash
helm delete todo-chatbot
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Configuration

The following table lists the configurable parameters of the todo-chatbot chart and their default values.

### Global Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `global.imagePullPolicy` | Image pull policy | `"IfNotPresent"` |
| `global.imagePullSecrets` | Image pull secrets | `[]` |

### Backend Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backend.replicaCount` | Number of backend pods | `1` |
| `backend.image.repository` | Backend image repository | `"todo-backend"` |
| `backend.image.tag` | Backend image tag | `"latest"` |
| `backend.image.pullPolicy` | Backend image pull policy | `"IfNotPresent"` |
| `backend.service.type` | Backend service type | `"ClusterIP"` |
| `backend.service.port` | Backend service port | `8000` |
| `backend.resources.limits.cpu` | Backend CPU limit | `"500m"` |
| `backend.resources.limits.memory` | Backend memory limit | `"512Mi"` |
| `backend.resources.requests.cpu` | Backend CPU request | `"100m"` |
| `backend.resources.requests.memory` | Backend memory request | `"128Mi"` |

### Frontend Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `frontend.replicaCount` | Number of frontend pods | `1` |
| `frontend.image.repository` | Frontend image repository | `"todo-frontend"` |
| `frontend.image.tag` | Frontend image tag | `"latest"` |
| `frontend.image.pullPolicy` | Frontend image pull policy | `"IfNotPresent"` |
| `frontend.service.type` | Frontend service type | `"ClusterIP"` |
| `frontend.service.port` | Frontend service port | `3000` |
| `frontend.resources.limits.cpu` | Frontend CPU limit | `"200m"` |
| `frontend.resources.limits.memory` | Frontend memory limit | `"256Mi"` |
| `frontend.resources.requests.cpu` | Frontend CPU request | `"50m"` |
| `frontend.resources.requests.memory` | Frontend memory request | `"64Mi"` |

### Ingress Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.className` | Ingress class name | `""` |
| `ingress.hosts[0].host` | Hostname for ingress | `"todo-chatbot.local"` |
| `ingress.hosts[0].paths[0].path` | Path for ingress | `"/"` |
| `ingress.hosts[0].paths[0].pathType` | Path type for ingress | `"Prefix"` |

## Example Usage

### Custom Values

```yaml
backend:
  replicaCount: 2
  resources:
    limits:
      cpu: "1000m"
      memory: "1Gi"
    requests:
      cpu: "200m"
      memory: "256Mi"

frontend:
  replicaCount: 2
  resources:
    limits:
      cpu: "500m"
      memory: "512Mi"
    requests:
      cpu: "100m"
      memory: "128Mi"

ingress:
  hosts:
    - host: "my-todo-app.example.com"
      paths:
        - path: /
          pathType: Prefix
```

## Architecture

The chart deploys:

1. Two Deployments (one for backend, one for frontend)
2. Two Services (one for backend, one for frontend)
3. An Ingress resource for external access
4. A ConfigMap for application configuration

## Development

To test the chart locally:

```bash
# Dry run installation
helm install todo-chatbot . --dry-run --debug

# Lint the chart
helm lint .

# Template verification
helm template todo-chatbot .
```

## Troubleshooting

### Pods not starting

Check the pod status and logs:
```bash
kubectl get pods
kubectl logs -l app=todo-backend
kubectl logs -l app=todo-frontend
```

### Ingress not accessible

Verify ingress is created and has an address:
```bash
kubectl get ingress
minikube service todo-chatbot-frontend-svc --url
```

### Resource limits

Adjust resource requests and limits in values.yaml based on your cluster's capacity.