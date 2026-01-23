# Research Document: Phase-IV Kubernetes Deployment

## Decision: Dockerfile Base Images and Multi-Stage Build Choices

**Rationale**: For the FastAPI backend, using Python 3.13-alpine as the base image provides the smallest footprint while maintaining compatibility. For the Next.js frontend, using node:20-alpine as the base image balances size and compatibility. Multi-stage builds will separate dependency installation from runtime to minimize final image size.

**Alternatives considered**:
- Python slim images: Larger than alpine but more stable
- Node slim images: Larger than alpine but with more system libraries
- Distroless images: Smallest possible but harder to debug
- Ubuntu base: Larger but more compatible with complex dependencies

**Decision**: Use Alpine-based images for both backend and frontend to achieve the sub-500MB target while maintaining compatibility.

## Decision: Helm Chart Structure

**Rationale**: Single Helm chart approach is chosen to simplify deployment and management. This allows deploying the entire application with a single `helm install` command while keeping all related resources together.

**Alternatives considered**:
- Separate charts for frontend and backend: More modular but increases deployment complexity
- Monorepo with subcharts: Could reuse components but adds complexity
- Single chart (selected): Simplifies deployment and reduces coordination overhead

**Decision**: Single Helm chart with templates for both frontend and backend deployments, services, and ingress.

## Decision: Minikube Configuration

**Rationale**: Using Docker driver with 2 CPU, 2GB RAM, and 10GB disk aligns with the specified resource constraints and provides optimal performance on WSL2/Linux systems. The 10GB limit ensures compatibility with limited C: drive space.

**Alternatives considered**:
- VirtualBox driver: Cross-platform but heavier overhead
- HyperKit driver: macOS specific
- KVM2 driver: Linux specific with better performance
- Docker driver (selected): Works well on Windows with WSL2, efficient resource usage

**Decision**: Docker driver with --cpus=2 --memory=2gb --disk-size=10g configuration.

## Decision: Image Pull Strategy

**Rationale**: Using local build strategy (minikube image build) is most appropriate for local development. This avoids Docker Hub rate limits and ensures the latest code changes are included without pushing to a registry.

**Alternatives considered**:
- Pre-built images from Docker Hub: Faster initial deployment but harder to customize
- Local build (selected): Ensures latest code, avoids registry dependencies
- Private registry: Production-like but adds complexity for local dev

**Decision**: Use minikube's built-in Docker daemon for building images locally.

## Decision: Ingress Setup for Minikube

**Rationale**: Using NGINX Ingress Controller with minikube's ingress addon provides a production-like experience while being simple to configure. The default minikube IP with port forwarding handles external access.

**Alternatives considered**:
- NodePort service: Simpler but less flexible
- LoadBalancer service: Requires cloud provider or metallb
- Ingress with addon (selected): Provides production-like routing, supports path-based routing
- Port forwarding: Manual and not scalable

**Decision**: Enable minikube ingress addon and configure NGINX ingress for routing to frontend and backend services.

## Decision: Referencing Phase-II-full-stack-todo Code

**Rationale**: Using build contexts that point to the existing phase-II-full-stack-todo directory while building Docker images ensures the code remains unmodified while being properly included in the container.

**Alternatives considered**:
- Copying code to new directory: Violates requirement to keep original unchanged
- Git submodules: Adds complexity
- Build context references (selected): Maintains original code integrity while allowing access during build
- Volume mounts: Runtime only, not for container building

**Decision**: Use Docker build contexts that reference the existing phase-II-full-stack-todo directory structure without copying or modifying it.