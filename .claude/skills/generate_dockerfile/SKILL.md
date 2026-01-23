---
name: generate_dockerfile
description: Generate secure, production-ready multi-stage Dockerfiles and .dockerignore for Phase-IV Todo Chatbot deployment. Creates files only in phase-II-full-stack-todo/docker/ — never touches existing Phase-III code or specs.
---
# Dockerfile Generation Skill for Phase-IV

## Instructions
1. **Backend (FastAPI)**
   - Base: python:3.13-slim
   - Multi-stage: builder + runtime
   - Install uvicorn, SQLModel, asyncpg
   - Non-root user (appuser)
   - Expose 8000

2. **Frontend (Next.js)**
   - Base: node:20-slim
   - Multi-stage: build + runner
   - Standalone mode
   - Non-root user (node)
   - Expose 3000

3. **.dockerignore**
   - Common for both
   - Exclude node_modules, __pycache__, .git, tests, etc.

## Best Practices
- Always multi-stage builds
- Non-root user (USER node or appuser)
- Minimal final image size (<300MB target)
- Copy dependency files first for caching
- No dev dependencies in runtime stage
- Use .dockerignore to reduce context
- Add HEALTHCHECK if possible
- Label images with version

## Example Structure

### Backend Dockerfile
```dockerfile
# Dockerfile.backend
FROM python:3.13-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim

RUN useradd -m appuser
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY . .

USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile
```dockerfile
# Dockerfile.frontend
FROM node:20-slim AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-slim AS runner

RUN useradd -m node
WORKDIR /app
COPY --chown=node:node . .
COPY --from=builder --chown=node:node /app/node_modules ./node_modules

USER node
EXPOSE 3000
HEALTHCHECK --interval=30s CMD curl -f http://localhost:3000/health || exit 1
CMD ["npm", "start"]
```

### .dockerignore
```
# .dockerignore
node_modules
__pycache__
*.pyc
*.pyo
*.pyd
.Python
.cache
.venv
venv/
env/
ENV/
dist/
build/
*.egg-info/
.nyc_output/
coverage/
logs
*.log
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
.git
.gitignore
README.md
Dockerfile*
.dockerignore
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
.env.*
.coverage
htmlcov/
.pytest_cache/
.hypothesis/
.vscode
.idea
*.swp
*.swo
*~
.nuxt
.next
public/build/
out/
.npm
.yarn
*.tmp
*.temp
tmp/
temp/
```