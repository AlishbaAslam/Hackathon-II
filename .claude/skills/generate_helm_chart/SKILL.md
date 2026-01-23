---
name: generate_helm_chart
description: Generate a complete, production-ready Helm 3 chart for Phase-IV Kubernetes deployment of the Todo Chatbot (FastAPI backend + Next.js frontend) on Minikube. Files are created only in phase-II-full-stack-todo/helm/todo-chart/ and never modify existing Phase-III code or specs.
---
# Helm Chart Generation Skill for Phase-IV

## Instructions
1. **Chart Structure**
   - Create Chart.yaml with name, version, description
   - Generate configurable values.yaml (replicas, images, ports, ingress.host)
   - Create templates folder with Deployment, Service, Ingress

2. **Backend & Frontend**
   - Separate Deployments for backend (port 8000) and frontend (port 3000)
   - Use images: todo-backend:latest and todo-frontend:latest
   - Configurable replicas (default 1)

3. **Minikube Compatibility**
   - Ingress with host todo.local
   - Service type ClusterIP
   - No external dependencies

## Best Practices
- Use Helm 3 syntax and helpers
- Make all important values configurable in values.yaml
- Use named templates for reusable blocks
- Add comments in templates
- Set default replicas=1 for low-resource Minikube
- Use ingress.host=todo.local (Minikube addon)
- Validate with helm lint / helm template
- Keep chart simple and focused on deployment

## Example Structure

### Chart.yaml
```yaml
apiVersion: v2
name: todo-chart
description: Helm chart for Todo Chatbot (FastAPI + Next.js) on Minikube
type: application
version: 0.1.0
appVersion: "1.0"
```

### values.yaml
```yaml
# Default values for todo-chart
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

backend:
  image:
    repository: todo-backend
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 8000
  replicaCount: 1
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 100m
      memory: 128Mi

frontend:
  image:
    repository: todo-frontend
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 3000
  replicaCount: 1
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 100m
      memory: 128Mi

ingress:
  enabled: true
  className: ""
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
  hosts:
    - host: todo.local
      paths:
        - path: /
          pathType: Prefix
  tls: []
```

### templates/_helpers.tpl
```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "todo-chart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "todo-chart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "todo-chart.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo-chart.labels" -}}
helm.sh/chart: {{ include "todo-chart.chart" . }}
{{ include "todo-chart.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "todo-chart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

### templates/backend-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-chart.fullname" . }}-backend
  labels:
    {{- include "todo-chart.labels" . | nindent 4 }}
    app: backend
spec:
  replicas: {{ .Values.backend.replicaCount }}
  selector:
    matchLabels:
      {{- include "todo-chart.selectorLabels" . | nindent 6 }}
      app: backend
  template:
    metadata:
      labels:
        {{- include "todo-chart.selectorLabels" . | nindent 8 }}
        app: backend
    spec:
      containers:
        - name: backend
          image: "{{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag }}"
          imagePullPolicy: {{ .Values.backend.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 8000
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            {{- toYaml .Values.backend.resources | nindent 12 }}
```

### templates/backend-service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "todo-chart.fullname" . }}-backend
  labels:
    {{- include "todo-chart.labels" . | nindent 4 }}
    app: backend
spec:
  type: {{ .Values.backend.service.type }}
  ports:
    - port: {{ .Values.backend.service.port }}
      targetPort: 8000
      protocol: TCP
      name: http
  selector:
    {{- include "todo-chart.selectorLabels" . | nindent 4 }}
    app: backend
```

### templates/frontend-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-chart.fullname" . }}-frontend
  labels:
    {{- include "todo-chart.labels" . | nindent 4 }}
    app: frontend
spec:
  replicas: {{ .Values.frontend.replicaCount }}
  selector:
    matchLabels:
      {{- include "todo-chart.selectorLabels" . | nindent 6 }}
      app: frontend
  template:
    metadata:
      labels:
        {{- include "todo-chart.selectorLabels" . | nindent 8 }}
        app: frontend
    spec:
      containers:
        - name: frontend
          image: "{{ .Values.frontend.image.repository }}:{{ .Values.frontend.image.tag }}"
          imagePullPolicy: {{ .Values.frontend.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 3000
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            {{- toYaml .Values.frontend.resources | nindent 12 }}
```

### templates/frontend-service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "todo-chart.fullname" . }}-frontend
  labels:
    {{- include "todo-chart.labels" . | nindent 4 }}
    app: frontend
spec:
  type: {{ .Values.frontend.service.type }}
  ports:
    - port: {{ .Values.frontend.service.port }}
      targetPort: 3000
      protocol: TCP
      name: http
  selector:
    {{- include "todo-chart.selectorLabels" . | nindent 4 }}
    app: frontend
```

### templates/ingress.yaml
```yaml
{{- if .Values.ingress.enabled -}}
{{- $fullName := include "todo-chart.fullname" . -}}
{{- $svcPort := .Values.frontend.service.port -}}
{{- if and .Values.ingress.className (not (hasKey .Values.ingress.annotations "kubernetes.io/ingress.class")) }}
{{- $_ := set .Values.ingress.annotations "kubernetes.io/ingress.class" .Values.ingress.className }}
{{- end }}
{{- if semverCompare ">=1.19-0" .Capabilities.KubeVersion.GitVersion -}}
apiVersion: networking.k8s.io/v1
{{- else if semverCompare ">=1.14-0" .Capabilities.KubeVersion.GitVersion -}}
apiVersion: networking.k8s.io/v1beta1
{{- else -}}
apiVersion: extensions/v1beta1
{{- end }}
kind: Ingress
metadata:
  name: {{ $fullName }}
  labels:
    {{- include "todo-chart.labels" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if and .Values.ingress.className (semverCompare ">=1.18-0" .Capabilities.KubeVersion.GitVersion) }}
  ingressClassName: {{ .Values.ingress.className }}
  {{- end }}
  {{- if .Values.ingress.tls }}
  tls:
    {{- range .Values.ingress.tls }}
    - hosts:
        {{- range .hosts }}
        - {{ . | quote }}
        {{- end }}
      secretName: {{ .secretName }}
    {{- end }}
  {{- end }}
  rules:
    {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            {{- if and .pathType (semverCompare ">=1.18-0" $.Capabilities.KubeVersion.GitVersion) }}
            pathType: {{ .pathType }}
            {{- else }}
            pathType: Prefix
            {{- end }}
            backend:
              {{- if semverCompare ">=1.19-0" $.Capabilities.KubeVersion.GitVersion }}
              service:
                name: {{ $fullName }}-frontend
                port:
                  number: {{ $svcPort }}
              {{- else }}
              serviceName: {{ $fullName }}-frontend
              servicePort: {{ $svcPort }}
              {{- end }}
          {{- end }}
    {{- end }}
{{- end }}
```

### NOTES.txt
```text
1. Get the application URL by running these commands:
{{- if .Values.ingress.enabled }}
{{- range $host := .Values.ingress.hosts }}
  http{{ if $.Values.ingress.tls }}s{{ end }}://{{ $host.host }}{{ range $host.paths }}{{ .path }}{{ end }}
{{- end }}
{{- else if contains "NodePort" .Values.frontend.service.type }}
  export NODE_PORT=$(kubectl get --namespace {{ .Release.Namespace }} -o jsonpath="{.spec.ports[0].nodePort}" services {{ include "todo-chart.fullname" . }}-frontend)
  export NODE_IP=$(kubectl get nodes --namespace {{ .Release.Namespace }} -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT
{{- else if contains "LoadBalancer" .Values.frontend.service.type }}
     NOTE: It may take a few minutes for the LoadBalancer IP to be available.
           You can watch the status of by running 'kubectl get --namespace {{ .Release.Namespace }} svc -w {{ include "todo-chart.fullname" . }}-frontend'
  export SERVICE_IP=$(kubectl get svc --namespace {{ .Release.Namespace }} {{ include "todo-chart.fullname" . }}-frontend --template "{{"{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}"}}")
  echo http://$SERVICE_IP:{{ .Values.frontend.service.port }}
{{- else if contains "ClusterIP" .Values.frontend.service.type }}
  export POD_NAME=$(kubectl get pods --namespace {{ .Release.Namespace }} -l "app=frontend,release={{ .Release.Name }}" -o jsonpath="{.items[0].metadata.name}")
  export CONTAINER_PORT=$(kubectl get pod --namespace {{ .Release.Namespace }} $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace {{ .Release.Namespace }} port-forward $POD_NAME 8080:$CONTAINER_PORT
{{- end }}
```