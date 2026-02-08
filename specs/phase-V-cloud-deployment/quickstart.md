# Quickstart Guide: Phase V - Advanced Cloud-Native Todo Chatbot

## Prerequisites

- **Docker Desktop** (with Kubernetes enabled) or **Minikube** installed
- **kubectl** (Kubernetes CLI)
- **Dapr CLI** installed (`dapr init`)
- **Helm 3** installed
- **Python 3.13+** with **uv** package manager
- **Node.js 20+** for frontend development
- **Redpanda Cloud Account** (for Kafka API compatibility)

## Setup Development Environment

### 1. Clone and Initialize Repository

```bash
# Clone the repository
git clone <your-repo-url>
cd todo-app

# Navigate to Phase V directory
cd specs/phase-V-cloud-deployment
```

### 2. Install Dapr and Initialize

```bash
# Initialize Dapr in Kubernetes
dapr init -k

# Verify Dapr installation
dapr status -k
```

### 3. Set Up Local Kafka (Development)

For development, you can use Redpanda locally:

```bash
# Deploy Redpanda to Kubernetes
kubectl create namespace redpanda
helm repo add redpandadata https://charts.redpanda.com
helm repo update
helm install redpanda redpandadata/redpanda -n redpanda --set console.enabled=true

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=redpanda -n redpanda --timeout=300s
```

### 4. Configure Dapr Components

Create the required Dapr components in the `phase-II-full-stack-todo/backend/dapr/components/` directory:

```bash
# Create components directory if it doesn't exist
mkdir -p phase-II-full-stack-todo/backend/dapr/components
```

#### Kafka Pub/Sub Component
Create `phase-II-full-stack-todo/backend/dapr/components/kafka-pubsub.yaml`:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "redpanda-redpanda-0.redpanda.redpanda.svc.cluster.local:9093"
  - name: consumerGroup
    value: "dapr-group"
  - name: authRequired
    value: "false"
```

#### State Store Component
Create `phase-II-full-stack-todo/backend/dapr/components/statestore.yaml`:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: "redis-master.redis.svc.cluster.local:6379"
  - name: redisPassword
    secretKeyRef:
      name: redis-password
      key: password
```

#### Secrets Component
Create `phase-II-full-stack-todo/backend/dapr/components/secrets.yaml`:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: secrets
spec:
  type: secretstores.kubernetes
  version: v1
  metadata: []
```

#### Apply Dapr Components

```bash
kubectl apply -f phase-II-full-stack-todo/backend/dapr/components/
```

## Running the Services Locally

### 1. Database Setup

First, set up your PostgreSQL database (Neon DB recommended):

```bash
# Create a new project in Neon DB and get your connection string
# Set environment variables
export DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
```

### 2. Backend Service with Dapr

```bash
# Navigate to backend directory
cd phase-II-full-stack-todo/backend

# Install dependencies
uv sync

# Run backend with Dapr sidecar
dapr run --app-id todo-api --app-port 8000 --dapr-http-port 3500 -- python -m src.main
```

### 3. Individual Microservices

Each service runs with its own Dapr sidecar:

#### Recurring Task Service
```bash
cd services/recurring-task-service
dapr run --app-id recurring-task-service --app-port 8001 -- python -m src.main
```

#### Notification Service
```bash
cd services/notification-service
dapr run --app-id notification-service --app-port 8002 -- python -m src.main
```

#### Audit Service
```bash
cd services/audit-service
dapr run --app-id audit-service --app-port 8003 -- python -m src.main
```

#### WebSocket Service
```bash
cd services/websocket-service
dapr run --app-id websocket-service --app-port 8004 -- python -m src.main
```

### 4. Frontend Service

```bash
cd phase-II-full-stack-todo/frontend
npm install
npm run dev
```

## Kubernetes Deployment

### 1. Build Docker Images

```bash
# Build backend image
docker build -f docker/Dockerfile.backend -t todo-backend:latest .

# Build frontend image
docker build -f docker/Dockerfile.frontend -t todo-frontend:latest .

# Build service images
docker build -f docker/Dockerfile.service-base -t recurring-task-service:latest ./services/recurring-task-service
docker build -f docker/Dockerfile.service-base -t notification-service:latest ./services/notification-service
docker build -f docker/Dockerfile.service-base -t audit-service:latest ./services/audit-service
docker build -f docker/Dockerfile.service-base -t websocket-service:latest ./services/websocket-service
```

### 2. Deploy to Minikube

```bash
# Start Minikube if not running
minikube start

# Deploy Kafka/Redpanda
kubectl create namespace kafka
helm install redpanda redpandadata/redpanda -n kafka

# Deploy Dapr
dapr init -k

# Deploy the application using Helm
helm install todo-app helm/todo-chart --namespace default --create-namespace
```

### 3. Access the Application

```bash
# Port forward to access the frontend
kubectl port-forward svc/todo-frontend 3000:80

# Access the backend API
kubectl port-forward svc/todo-backend 8000:80

# Access Dapr dashboard
dapr dashboard
```

## Testing the Event-Driven Architecture

### 1. Test Task Creation Flow

```bash
# Create a task via API
curl -X POST http://localhost:8000/api/users/test-user/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test recurring task",
    "description": "This is a test recurring task",
    "recurrence_pattern": {
      "type": "daily",
      "interval": 1,
      "end_condition": {"after_occurrences": 5}
    },
    "remind_at": "2026-02-04T10:00:00Z",
    "priority": "high",
    "tags": ["test", "recurring"]
  }'
```

### 2. Verify Event Processing

Check that events are published to Kafka and processed by the appropriate services:

```bash
# Monitor Dapr logs for event processing
dapr logs recurring-task-service -k
dapr logs notification-service -k
dapr logs audit-service -k
```

### 3. Test Real-time Sync

Open multiple browser windows to the frontend and verify that task changes appear in real-time across all clients via WebSocket connections.

## Key Configuration Files

### Environment Variables

Create `.env` files for each service:

**Backend (.env):**
```
DATABASE_URL=postgresql://...
SECRET_KEY=...
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DAPR_HTTP_ENDPOINT=http://localhost:3500
REDPANDA_BROKERS=localhost:9092
```

**Services (.env):**
```
DAPR_HTTP_ENDPOINT=http://localhost:3500
DATABASE_URL=postgresql://...
```

### Helm Values

Customize `helm/todo-chart/values.yaml` for your deployment:

```yaml
global:
  daprEnabled: true

todoApi:
  replicaCount: 1
  image:
    repository: todo-backend
    tag: latest
  service:
    port: 80

frontend:
  replicaCount: 1
  image:
    repository: todo-frontend
    tag: latest
  service:
    port: 80

recurringTaskService:
  replicaCount: 1
  image:
    repository: recurring-task-service
    tag: latest
  service:
    port: 8001

# Similar configurations for other services...
```

## Troubleshooting

### Common Issues

1. **Dapr Sidecar Not Starting**
   ```bash
   # Check Dapr status
   dapr status -k

   # Restart Dapr
   dapr uninstall -k
   dapr init -k
   ```

2. **Kafka Connection Issues**
   ```bash
   # Check Kafka pods
   kubectl get pods -n kafka

   # Check Kafka logs
   kubectl logs -l app.kubernetes.io/name=redpanda -n kafka
   ```

3. **Service Communication Failures**
   ```bash
   # Check service logs
   kubectl logs -l app=todo-api
   kubectl logs -l app=recurring-task-service

   # Check Dapr sidecar logs
   kubectl logs -l app=todo-api -c daprd
   ```

### Useful Commands

```bash
# Check all pods
kubectl get pods

# Check all services
kubectl get svc

# Check Dapr applications
dapr list -k

# Check Kafka topics
kubectl exec -it redpanda-redpanda-0 -n kafka -- rpk topic list

# Port forward for debugging
kubectl port-forward svc/redpanda-console -n kafka 8080:8080
```

## Next Steps

1. **Customize the Helm chart** for your specific cloud provider (OKE, AKS, GKE)
2. **Configure production secrets** and security settings
3. **Set up monitoring and logging** with Prometheus and Grafana
4. **Implement CI/CD pipeline** with GitHub Actions
5. **Scale services** based on your expected load
6. **Configure domain and SSL** for production deployment