---
id: PLAN-001
title: Phase V Plan Generated
stage: plan
feature: phase-V-cloud-deployment
date: 2026-02-03
status: completed
---

# Phase V Plan Generated

## Summary

Generated comprehensive implementation plan for Phase V: Advanced Cloud-Native Todo Chatbot with Kafka, Dapr & Real-time Sync. The plan outlines the technical architecture, data models, API contracts, and implementation roadmap for building an event-driven, cloud-native todo application with advanced features.

## Original Prompt

Phase V – Advanced Cloud-Native Todo Chatbot with Kafka, Dapr & Real-time Sync

Create:
- High-level architecture diagram (Mermaid or ASCII preferred)
- Folder & service structure overview (including how phase-II-full-stack-todo is extended)
- Step-by-step implementation roadmap (phases with clear order)
- Research & decision log
- Quality validation & testing strategy

Decisions needing documentation:
- Kafka choice: self-hosted Strimzi in Kubernetes vs Redpanda Cloud Serverless (free tier) vs other (tradeoffs: cost=0, setup time, Zookeeper need, learning curve, Dapr compatibility)
- Dapr vs direct Kafka/DB client libraries (tradeoffs: code simplicity, portability, vendor lock-in, debugging difficulty)
- Single repo approach (phase-V-cloud-deployment = copy of phase-II-full-stack-todo) vs separate microservices repos (tradeoffs: simplicity, git history, team collaboration)
- Real-time sync method: WebSocket vs Server-Sent Events vs polling (tradeoffs: latency, complexity, browser support, scalability)
- Reminder scheduling: Dapr Jobs API vs Kubernetes CronJob + DB polling (tradeoffs: exact timing, CPU overhead, scalability)
- Cloud provider: Oracle OKE (Always Free) vs Azure AKS (12 months free services) vs Google GKE ($300/90 days) (tradeoffs: free duration, resources given, setup complexity, long-term cost)

Technical details:
- Base codebase: phase-V-cloud-deployment (copy of phase-II-full-stack-todo with existing chatbot)
- Use agentic workflow: spec → plan → tasks → Claude Code implementation (no manual coding where possible)
- Use research-concurrent approach (look up Dapr/Kafka/Strimzi docs while implementing, not all upfront)
- Organize implementation in clear phases:
  1. Model & CRUD upgrade (add recurring, due_at, remind_at, priority, tags)
  2. Dapr + Kafka integration (Pub/Sub, Jobs, State, Secrets)
  3. Core services build (Recurring Task, Notification/Reminder, Audit/Logging, Real-time Sync)
  4. Frontend updates (UI + WebSocket real-time)
  5. Local Minikube deployment + Helm chart update + Dapr init -k
  6. Cloud path preparation (Oracle OKE recommended – Always Free)
  7. CI/CD outline with GitHub Actions
  8. Basic monitoring/logging recommendations
- Testing strategy:
  - Unit tests for each service (Pytest backend)
  - Integration tests: event publish → consume → action (e.g. complete recurring task → next created → notification sent → sync pushed)
  - End-to-end demo: task created in UI → real-time sync to other client → reminder triggered → audit logged
  - Validation checks against success criteria (recurring works, sync instant, logs complete, Dapr fully abstracted)

Output format:
- Start with Mermaid or ASCII architecture diagram
- Then folder structure & service overview
- Then phased roadmap (with estimated effort)
- Then decision log (choices + tradeoffs table)
- End with testing strategy & quality validation checklist

## Response Summary

Successfully created comprehensive implementation plan at `/mnt/d/Hackathon-II/todo-app/specs/phase-V-cloud-deployment/plan.md` with:

- Detailed architecture diagram showing all services and interactions
- Complete technical context with technology stack and constraints
- Extensive project structure outlining all directories and components
- 5-phase implementation roadmap with clear ordering
- Decision log documenting all key technology choices with tradeoff analysis
- Complete testing strategy for unit, integration, and end-to-end tests

Additional supporting documents created:
- Research document (`research.md`) with detailed technology analysis
- Data model (`data-model.md`) with enhanced entity definitions
- Quickstart guide (`quickstart.md`) for developers
- API contracts (`contracts/`) for all 5 services in OpenAPI format

## Key Architecture Decisions

- **Kafka**: Redpanda Cloud Serverless for development (free tier)
- **Dapr**: Used for all service communication to prevent vendor lock-in
- **Single Repo**: Monorepo approach for simplicity and coordination
- **WebSocket**: For real-time synchronization with low latency
- **Dapr Jobs API**: For exact-time reminder scheduling
- **Oracle OKE**: Recommended for free, sustainable cloud deployment

## Implementation Phases

1. Research & Architecture Design
2. Data Model & Service Contracts
3. Core Infrastructure Setup
4. Service Development (5 specialized services)
5. Frontend Updates
6. Deployment & Testing

## Status

Implementation plan is complete and approved for progression to the tasks generation phase.