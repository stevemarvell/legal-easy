# Deployment Guide

This guide covers deploying the AI Legal Platform API to various environments.

## Prerequisites

- Python 3.8+
- pip or poetry for dependency management
- Access to deployment environment (local, cloud, etc.)

## Local Development

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-legal-platform/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the development server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Development Configuration

Create a `.env` file for local development:

```env
# Development settings
DEBUG=true
LOG_LEVEL=debug
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Database (if applicable)
DATABASE_URL=sqlite:///./legal_platform.db

# API Configuration
API_VERSION=1.0.0
API_TITLE=AI Legal Platform API (Development)
```

## Production Deployment

### Environment Variables

Set these environment variables in production:

```env
# Production settings
DEBUG=false
LOG_LEVEL=info
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# API Configuration
API_VERSION=1.0.0
API_TITLE=AI Legal Platform API
```

### Docker Deployment

#### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=false
      - LOG_LEVEL=info
      - DATABASE_URL=postgresql://postgres:password@db:5432/legal_platform
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=legal_platform
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
    restart: unless-stopped

volumes:
  postgres_data:
```

#### Build and Run

```bash
# Build the image
docker build -t ai-legal-platform-api .

# Run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f api
```

### Cloud Deployment

#### AWS ECS

1. **Create ECR repository**
   ```bash
   aws ecr create-repository --repository-name ai-legal-platform-api
   ```

2. **Build and push image**
   ```bash
   # Get login token
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

   # Build and tag
   docker build -t ai-legal-platform-api .
   docker tag ai-legal-platform-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-legal-platform-api:latest

   # Push
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-legal-platform-api:latest
   ```

3. **Create ECS task definition**
   ```json
   {
     "family": "ai-legal-platform-api",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "256",
     "memory": "512",
     "executionRoleArn": "arn:aws:iam::<account-id>:role/ecsTaskExecutionRole",
     "containerDefinitions": [
       {
         "name": "api",
         "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-legal-platform-api:latest",
         "portMappings": [
           {
             "containerPort": 8000,
             "protocol": "tcp"
           }
         ],
         "environment": [
           {
             "name": "DEBUG",
             "value": "false"
           }
         ],
         "logConfiguration": {
           "logDriver": "awslogs",
           "options": {
             "awslogs-group": "/ecs/ai-legal-platform-api",
             "awslogs-region": "us-east-1",
             "awslogs-stream-prefix": "ecs"
           }
         }
       }
     ]
   }
   ```

#### Google Cloud Run

1. **Build and push to Container Registry**
   ```bash
   # Configure Docker
   gcloud auth configure-docker

   # Build and tag
   docker build -t gcr.io/your-project-id/ai-legal-platform-api .

   # Push
   docker push gcr.io/your-project-id/ai-legal-platform-api
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy ai-legal-platform-api \
     --image gcr.io/your-project-id/ai-legal-platform-api \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8000 \
     --set-env-vars DEBUG=false,LOG_LEVEL=info
   ```

#### Heroku

1. **Create Heroku app**
   ```bash
   heroku create ai-legal-platform-api
   ```

2. **Set environment variables**
   ```bash
   heroku config:set DEBUG=false
   heroku config:set LOG_LEVEL=info
   ```

3. **Create Procfile**
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

### Kubernetes Deployment

#### Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-legal-platform-api
  labels:
    app: ai-legal-platform-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-legal-platform-api
  template:
    metadata:
      labels:
        app: ai-legal-platform-api
    spec:
      containers:
      - name: api
        image: ai-legal-platform-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DEBUG
          value: "false"
        - name: LOG_LEVEL
          value: "info"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: ai-legal-platform-api-service
spec:
  selector:
    app: ai-legal-platform-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```

#### Deploy to Kubernetes

```bash
# Apply deployment
kubectl apply -f deployment.yaml

# Check status
kubectl get pods
kubectl get services

# View logs
kubectl logs -f deployment/ai-legal-platform-api
```

## Monitoring and Logging

### Health Checks

The API includes a health check endpoint at `/health`:

```json
{
  "status": "healthy",
  "service": "AI Legal Platform API"
}
```

### Logging Configuration

Configure logging in production:

```python
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
```

### Monitoring Tools

- **Prometheus**: For metrics collection
- **Grafana**: For visualization
- **ELK Stack**: For log aggregation
- **Sentry**: For error tracking

## Security Considerations

### HTTPS/TLS

Always use HTTPS in production:

```nginx
server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    location / {
        proxy_pass http://api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Environment Variables

Never commit sensitive information:

- Use environment variables for secrets
- Use secret management services (AWS Secrets Manager, etc.)
- Rotate secrets regularly

### CORS Configuration

Configure CORS properly for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domains only
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## Performance Optimization

### Caching

Implement caching for frequently accessed data:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_case_statistics():
    # Expensive operation
    return calculate_statistics()
```

### Database Optimization

- Use connection pooling
- Implement proper indexing
- Use read replicas for read-heavy workloads

### Load Balancing

Use a load balancer to distribute traffic:

```nginx
upstream api_backend {
    server api1:8000;
    server api2:8000;
    server api3:8000;
}

server {
    location / {
        proxy_pass http://api_backend;
    }
}
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find process using port
   lsof -i :8000
   # Kill process
   kill -9 <PID>
   ```

2. **Module not found errors**
   ```bash
   # Ensure virtual environment is activated
   source .venv/bin/activate
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

3. **CORS errors**
   - Check CORS configuration
   - Verify allowed origins
   - Check preflight requests

### Debugging

Enable debug mode for development:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        debug=True,
        log_level="debug"
    )
```

### Log Analysis

Check application logs:

```bash
# Docker logs
docker logs <container-id>

# Kubernetes logs
kubectl logs -f deployment/ai-legal-platform-api

# System logs
tail -f /var/log/app.log
```

## Backup and Recovery

### Database Backups

```bash
# PostgreSQL backup
pg_dump -h localhost -U postgres legal_platform > backup.sql

# Restore
psql -h localhost -U postgres legal_platform < backup.sql
```

### File Backups

```bash
# Backup application files
tar -czf app-backup-$(date +%Y%m%d).tar.gz /app

# Backup to cloud storage
aws s3 cp backup.tar.gz s3://your-backup-bucket/
```

## Scaling

### Horizontal Scaling

- Use multiple API instances behind a load balancer
- Implement stateless design
- Use external session storage

### Vertical Scaling

- Increase CPU and memory resources
- Optimize database queries
- Use caching strategies

### Auto-scaling

Configure auto-scaling based on metrics:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ai-legal-platform-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-legal-platform-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```