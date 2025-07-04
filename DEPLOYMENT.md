# Knowledge Management Agent - Deployment Guide

## Quick Start Options

### Option 1: Docker (Recommended)
The fastest way to get started with the complete system:

```bash
# Clone or create the project
git clone <repository-url>
cd knowledge-management-agent

# Start all services
docker-compose up -d

# Access the application
open http://localhost:8000
```

This will start:
- Neo4j database on port 7474 (web interface) and 7687 (bolt)
- Knowledge Management Agent on port 8000

### Option 2: Manual Installation
For development or custom setups:

```bash
# 1. Install dependencies
python setup.py

# 2. Start Neo4j (choose one):
# - Docker: docker run -d -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:5.15
# - Local installation: Download from https://neo4j.com/download/

# 3. Configure environment
cp .env.example .env
# Edit .env with your Neo4j credentials

# 4. Start the application
source venv/bin/activate
uvicorn app.main:app --reload

# 5. Access the application
open http://localhost:8000
```

## Production Deployment

### Docker Swarm
```bash
# For production with Docker Swarm
docker stack deploy -c docker-compose.yml knowledge-agent
```

### Kubernetes
```yaml
# Example k8s deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: knowledge-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: knowledge-agent
  template:
    metadata:
      labels:
        app: knowledge-agent
    spec:
      containers:
      - name: knowledge-agent
        image: knowledge-agent:latest
        ports:
        - containerPort: 8000
        env:
        - name: NEO4J_URI
          value: "bolt://neo4j-service:7687"
```

### Cloud Deployment

#### AWS
```bash
# Using AWS ECS
aws ecs create-cluster --cluster-name knowledge-agent-cluster
# Deploy using ECS task definition
```

#### Google Cloud
```bash
# Using Cloud Run
gcloud run deploy knowledge-agent --image=gcr.io/PROJECT_ID/knowledge-agent
```

#### Azure
```bash
# Using Container Instances
az container create --resource-group myResourceGroup --name knowledge-agent
```

## Configuration

### Environment Variables
Create a `.env` file with:

```bash
# Neo4j Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_secure_password

# Optional: OpenAI for enhanced NLP
OPENAI_API_KEY=your_openai_key

# Application Settings
DEBUG=false
LOG_LEVEL=INFO
```

### Neo4j Configuration
For production Neo4j setup:

```bash
# neo4j.conf optimizations
dbms.memory.heap.initial_size=512m
dbms.memory.heap.max_size=2G
dbms.memory.pagecache.size=1G
```

## Monitoring

### Health Checks
```bash
# Application health
curl http://localhost:8000/health

# Neo4j health
curl http://localhost:7474/db/manage/server/version
```

### Logging
Logs are available at:
- Application: stdout/stderr
- Neo4j: `/var/log/neo4j/` (in container)

### Metrics
Built-in endpoints:
- `/api/kg/stats` - Knowledge graph statistics
- `/api/chat/history` - Chat history

## Backup and Recovery

### Neo4j Backup
```bash
# Create backup
docker exec neo4j-container neo4j-admin backup --backup-dir=/backups

# Restore backup
docker exec neo4j-container neo4j-admin restore --from=/backups/backup-name
```

### Data Export
```bash
# Export knowledge graph
curl -X GET http://localhost:8000/api/kg/ > knowledge-graph.json
```

## Security

### Authentication
Add authentication middleware:

```python
# app/middleware/auth.py
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def authenticate(token: str = Depends(security)):
    # Implement your authentication logic
    pass
```

### HTTPS
Use a reverse proxy like Nginx:

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Scaling

### Horizontal Scaling
- Run multiple application instances behind a load balancer
- Use Redis for session storage
- Scale Neo4j with clustering

### Vertical Scaling
- Increase memory allocation for Neo4j
- Add more CPU cores
- Use SSD storage for better performance

## Troubleshooting

### Common Issues

1. **Connection refused to Neo4j**
   ```bash
   # Check Neo4j status
   docker logs neo4j-container
   
   # Verify port binding
   netstat -tulpn | grep 7687
   ```

2. **Application won't start**
   ```bash
   # Check logs
   docker logs knowledge-agent-container
   
   # Test basic functionality
   python test_basic.py
   ```

3. **High memory usage**
   ```bash
   # Monitor Neo4j memory
   docker stats neo4j-container
   
   # Tune Neo4j settings
   # Edit docker-compose.yml environment variables
   ```

### Debug Mode
Enable debug mode for detailed logging:

```bash
# In .env file
DEBUG=true
LOG_LEVEL=DEBUG
```

## Performance Optimization

### Database Optimization
```cypher
# Create indexes for better performance
CREATE INDEX entity_name_index FOR (e:Entity) ON (e.name);
CREATE INDEX entity_type_index FOR (e:Entity) ON (e.type);
```

### Application Optimization
- Use connection pooling
- Implement caching for frequent queries
- Optimize batch operations

### Frontend Optimization
- Implement pagination for large graphs
- Use WebSockets for real-time updates
- Add client-side caching

## Updates and Maintenance

### Updating the Application
```bash
# Pull latest changes
git pull origin main

# Rebuild containers
docker-compose down
docker-compose up -d --build
```

### Database Maintenance
```bash
# Regular maintenance
docker exec neo4j-container neo4j-admin check-consistency

# Compact database
docker exec neo4j-container neo4j-admin compact
```

This deployment guide covers the essential steps to get your Knowledge Management Agent running in various environments, from local development to production deployments.