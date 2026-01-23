# Data Model: Phase-IV Kubernetes Deployment

## Kubernetes Resource Entities

### Deployment
- **Name**: Represents the Kubernetes Deployment resource
- **Fields**:
  - apiVersion: apps/v1
  - kind: Deployment
  - metadata.name: unique deployment identifier
  - metadata.namespace: optional namespace (default: default)
  - spec.replicas: number of pod replicas
  - spec.selector.matchLabels: pod selector labels
  - spec.template.metadata.labels: pod labels
  - spec.template.spec.containers: list of containers
- **Relationships**: Contains multiple Pod instances
- **Validation**: Must specify at least one container, replica count must be >= 0

### Service
- **Name**: Represents the Kubernetes Service resource
- **Fields**:
  - apiVersion: v1
  - kind: Service
  - metadata.name: unique service identifier
  - spec.selector: pod selector
  - spec.ports: list of exposed ports
  - spec.type: Service type (ClusterIP, NodePort, LoadBalancer)
- **Relationships**: Routes traffic to Deployment pods
- **Validation**: Must specify valid port ranges (1-65535), service type must be valid

### Ingress
- **Name**: Represents the Kubernetes Ingress resource
- **Fields**:
  - apiVersion: networking.k8s.io/v1
  - kind: Ingress
  - metadata.name: unique ingress identifier
  - spec.rules: list of routing rules
  - spec.tls: optional TLS configuration
- **Relationships**: Routes external traffic to Services
- **Validation**: Rules must specify valid hostnames and paths

### ConfigMap
- **Name**: Represents the Kubernetes ConfigMap resource
- **Fields**:
  - apiVersion: v1
  - kind: ConfigMap
  - metadata.name: unique configmap identifier
  - data: key-value pairs of configuration data
- **Relationships**: Referenced by Deployments for configuration
- **Validation**: Keys must be valid DNS subdomain names, values must be strings

## Helm Chart Entities

### Chart
- **Name**: Represents the Helm Chart package
- **Fields**:
  - apiVersion: Helm chart API version
  - name: chart name
  - version: chart version
  - description: chart description
  - dependencies: list of chart dependencies
- **Relationships**: Contains multiple templates and default values
- **Validation**: Must have valid semver version, required fields must be present

### Template
- **Name**: Represents a Helm template file
- **Fields**:
  - filename: name of the template file
  - content: Go template syntax with Kubernetes resource definitions
  - parameters: values that can be customized
- **Relationships**: Part of a Chart, generates Kubernetes resources
- **Validation**: Must be valid YAML after template substitution

### Values
- **Name**: Represents configurable parameters for a Helm chart
- **Fields**:
  - parameters: key-value pairs of configurable settings
  - types: data types for each parameter
  - defaults: default values for each parameter
- **Relationships**: Used by Templates to customize resource definitions
- **Validation**: Must match expected data types, required values must be provided