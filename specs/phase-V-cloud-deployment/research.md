# Research Document: Phase V - Advanced Cloud-Native Todo Chatbot with Kafka, Dapr & Real-time Sync

## Kafka Choice Analysis

### Options Evaluated

#### 1. Self-hosted Strimzi in Kubernetes
- **Cost**: $0 (self-hosted)
- **Setup Time**: High (requires Kafka/Zookeeper cluster setup)
- **Zookeeper Need**: Yes (traditional Kafka requires Zookeeper or Kraft mode)
- **Learning Curve**: High (complex configuration)
- **Dapr Compatibility**: Excellent
- **Pros**: Full control, production-ready, extensive configuration options
- **Cons**: Complex setup, resource-intensive, steep learning curve

#### 2. Redpanda Cloud Serverless (Free Tier)
- **Cost**: $0 (generous free tier)
- **Setup Time**: Minimal (just API keys)
- **Zookeeper Need**: No (Redpanda is Kafka-API compatible without Zookeeper)
- **Learning Curve**: Low (simple configuration)
- **Dapr Compatibility**: Excellent (Kafka API compatible)
- **Pros**: Zero setup, no Zookeeper, cost-effective, excellent performance
- **Cons**: Vendor lock-in risk, limited by free tier constraints

#### 3. Confluent Cloud
- **Cost**: Paid (limited free tier)
- **Setup Time**: Low (managed service)
- **Zookeeper Need**: No (managed)
- **Learning Curve**: Medium
- **Dapr Compatibility**: Excellent
- **Pros**: Enterprise features, excellent support
- **Cons**: Costlier, potential vendor lock-in

### Recommendation: Redpanda Cloud Serverless
**Rationale**: For Phase V development and testing, Redpanda's free tier offers the best balance of simplicity and functionality. It provides Kafka API compatibility without the complexity of Zookeeper, making it ideal for rapid development and validation. The Dapr compatibility is excellent, and the zero-setup requirement accelerates development.

## Dapr vs Direct Kafka/DB Client Libraries

### Dapr Approach
- **Code Simplicity**: Moderate (additional Dapr SDK integration)
- **Portability**: High (vendor-neutral abstraction)
- **Vendor Lock-in**: Low (abstraction layer)
- **Debugging Difficulty**: Higher (additional layer of complexity)
- **Maintenance**: Lower (managed by Dapr runtime)

### Direct Client Libraries
- **Code Simplicity**: High (direct API calls)
- **Portability**: Low (tied to specific implementations)
- **Vendor Lock-in**: High (tight coupling to Kafka/DB)
- **Debugging Difficulty**: Lower (fewer layers)
- **Maintenance**: Higher (application-level connection management)

### Recommendation: Use Dapr
**Rationale**: The Phase V requirements specifically emphasize using Dapr for abstraction to prevent vendor lock-in. The slight increase in complexity is offset by the significant benefits of portability and the ability to swap underlying implementations (Kafka can be replaced with Redpanda, RabbitMQ, etc.).

## Single Repo vs Separate Microservices Repos

### Single Repo Approach (Monorepo)
- **Simplicity**: High (single codebase, unified CI/CD)
- **Git History**: Preserved (all changes in one place)
- **Team Collaboration**: Moderate (potential for merge conflicts)
- **Development Speed**: High (no cross-repo coordination)
- **Complexity**: Moderate (larger codebase)

### Separate Microservices Repos
- **Simplicity**: Low (multiple repositories to manage)
- **Git History**: Distributed (scattered across repos)
- **Team Collaboration**: High (teams can work independently)
- **Development Speed**: Lower (cross-repo coordination needed)
- **Complexity**: High (multiple CI/CD pipelines, version management)

### Recommendation: Single Repo Approach
**Rationale**: For Phase V, where the goal is to extend the existing phase-II-full-stack-todo with advanced features, a monorepo approach maintains continuity and simplifies the development process. It allows for coordinated changes across services while maintaining clear separation of concerns within the repository structure.

## Real-time Sync Method Selection

### WebSocket
- **Latency**: Very Low (bidirectional, persistent connection)
- **Complexity**: Medium (connection management, error handling)
- **Browser Support**: Excellent (modern browsers)
- **Scalability**: Good (connection pooling, load balancing)
- **Resource Usage**: Moderate (persistent connections)

### Server-Sent Events (SSE)
- **Latency**: Low (server pushes to client)
- **Complexity**: Low (simpler than WebSocket)
- **Browser Support**: Good (most modern browsers)
- **Scalability**: Good (HTTP-based)
- **Resource Usage**: Low
- **Limitation**: Unidirectional (server to client only)

### Polling
- **Latency**: High (depends on polling interval)
- **Complexity**: Low (standard HTTP requests)
- **Browser Support**: Excellent (all browsers)
- **Scalability**: Poor (high server load)
- **Resource Usage**: High (frequent requests)

### Recommendation: WebSocket
**Rationale**: The requirements specify real-time multi-client sync via WebSocket. WebSocket provides true bidirectional communication with low latency, which is essential for real-time task synchronization across multiple clients. While more complex than SSE, it provides the necessary functionality for the real-time sync requirements.

## Reminder Scheduling Options

### Dapr Jobs API
- **Exact Timing**: Yes (precise scheduling)
- **CPU Overhead**: Low (external scheduler)
- **Scalability**: High (distributed scheduling)
- **Integration**: Excellent (native Dapr component)
- **Reliability**: High (managed by Dapr)

### Kubernetes CronJob + DB Polling
- **Exact Timing**: Moderate (dependent on CronJob precision)
- **CPU Overhead**: Medium (polling service required)
- **Scalability**: Good (Kubernetes native)
- **Integration**: Moderate (requires custom polling logic)
- **Reliability**: Good (Kubernetes managed)

### Recommendation: Dapr Jobs API
**Rationale**: The requirements specifically mention using Dapr Jobs API for exact-time reminders. This approach provides precise scheduling capabilities with excellent integration into the Dapr ecosystem. It also aligns with the overall architecture decision to use Dapr for all service communications.

## Cloud Provider Selection

### Oracle OKE (Always Free)
- **Free Duration**: Indefinite (Always Free tier)
- **Resources Given**: Generous for basic usage
- **Setup Complexity**: Moderate
- **Long-term Cost**: $0 for basic usage
- **Features**: Standard Kubernetes features

### Azure AKS (12 Months Free)
- **Free Duration**: 12 months
- **Resources Given**: Good for trial period
- **Setup Complexity**: Low to Moderate
- **Long-term Cost**: Pay-as-you-go after 12 months
- **Features**: Enterprise-grade features

### Google GKE ($300/90 Days)
- **Free Duration**: 90 days (with credits)
- **Resources Given**: $300 credit for 90 days
- **Setup Complexity**: Moderate
- **Long-term Cost**: Pay-as-you-go after credits
- **Features**: Full enterprise features

### Recommendation: Oracle OKE
**Rationale**: The requirements specifically recommend Oracle OKE for the Always Free tier. This provides long-term sustainability for the project without cost concerns. Combined with Dapr's portability, this choice maintains flexibility to migrate to other providers if needed in the future.

## Event Schema Design

### Task Events Topic
```
{
  "eventId": "uuid",
  "eventType": "task.created | task.updated | task.completed | task.deleted | task.recurring.completed",
  "userId": "string",
  "taskId": "int",
  "timestamp": "datetime",
  "payload": {
    // Task object with all properties
  }
}
```

### Reminders Topic
```
{
  "eventId": "uuid",
  "eventType": "reminder.scheduled | reminder.triggered | reminder.cancelled",
  "userId": "string",
  "taskId": "int",
  "scheduledTime": "datetime",
  "timestamp": "datetime",
  "payload": {
    // Reminder details
  }
}
```

### Task Updates Topic
```
{
  "eventId": "uuid",
  "eventType": "task.sync",
  "userId": "string",
  "taskId": "int",
  "timestamp": "datetime",
  "payload": {
    // Delta of changes or full task object
  }
}
```

## Dapr Component Configuration

### Kafka Pub/Sub Component
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
    value: "redpanda-cluster:9092"  # For local, or Redpanda cloud endpoint
  - name: consumerGroup
    value: "dapr-group"
  - name: authRequired
    value: "false"
```

### State Store Component
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: postgresql-state
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    secretKeyRef:
      name: postgresql-connection-string
  - name: actorStateStore
    value: "true"
```

### Jobs Component
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: jobs
spec:
  type: jobsscheduler.kubernetes
  version: v1
  metadata:
  - name: kubernetesConfig
    value: |
      namespace: default
```

## Technology Stack Summary

Based on research, the following technology stack is recommended for Phase V:

- **Core Backend**: FastAPI with Python 3.13+
- **Service Mesh**: Dapr 1.12+ for all inter-service communication
- **Message Queue**: Redpanda Cloud (Kafka API compatible)
- **Database**: PostgreSQL via Neon DB (serverless)
- **Frontend**: Next.js 16+ with WebSocket support
- **Orchestration**: Kubernetes (Minikube locally, OKE for cloud)
- **Real-time Sync**: WebSocket connections
- **Scheduling**: Dapr Jobs API
- **Monitoring**: Prometheus + Grafana (basic setup)
- **CI/CD**: GitHub Actions