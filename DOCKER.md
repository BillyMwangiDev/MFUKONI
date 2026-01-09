# Docker Deployment Guide - Mfukoni Finance Tracker

**Last Updated:** January 10, 2026

This guide explains how to deploy Mfukoni Finance Tracker using Docker.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Docker Compose](#docker-compose)
4. [Manual Docker Commands](#manual-docker-commands)
5. [Configuration](#configuration)
6. [Data Persistence](#data-persistence)
7. [Production Deployment](#production-deployment)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- **Docker Engine** 20.10 or higher
- **Docker Compose** 2.0 or higher (optional, but recommended)
- **Internet connection** for downloading the base image

**Verify Docker installation:**
```bash
docker --version
docker-compose --version
```

---

## Quick Start

### Option 1: Docker Compose (Recommended)

1. **Clone or download the project:**
```bash
git clone <repository-url>
cd MFUKONI
```

2. **Create environment file (optional):**
```bash
cp .env.example .env
# Edit .env with your production settings
```

3. **Build and start:**
```bash
docker-compose up -d
```

4. **Access the application:**
   - Open: http://localhost:8000
   - The custom RDBMS will auto-initialize on first run

5. **View logs:**
```bash
docker-compose logs -f web
```

6. **Stop:**
```bash
docker-compose down
```

### Option 2: Docker Commands

```bash
# Build image
docker build -t mfukoni:latest .

# Run container
docker run -d \
  --name mfukoni-web \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e DEBUG=False \
  -e SECRET_KEY=your-production-secret-key \
  --restart unless-stopped \
  mfukoni:latest

# View logs
docker logs -f mfukoni-web

# Stop
docker stop mfukoni-web
docker rm mfukoni-web
```

---

## Docker Compose

### Configuration

The `docker-compose.yml` file includes:
- Automatic container restart
- Health checks
- Volume mounting for data persistence
- Environment variable configuration
- Network isolation

### Custom Port

To run on a different port (e.g., 8080):

```bash
PORT=8080 docker-compose up -d
```

Or modify `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"
```

### Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
TIME_ZONE=Africa/Nairobi
LANGUAGE_CODE=en-us
PORT=8000
```

The docker-compose.yml will automatically use these values.

---

## Manual Docker Commands

### Build Image

```bash
docker build -t mfukoni:latest .
```

**Build for specific platform:**
```bash
# ARM64 (Apple Silicon, Raspberry Pi)
docker buildx build --platform linux/arm64 -t mfukoni:latest .

# AMD64 (Intel/AMD)
docker buildx build --platform linux/amd64 -t mfukoni:latest .

# Multi-platform
docker buildx build --platform linux/amd64,linux/arm64 -t mfukoni:latest .
```

### Run Container

**Basic:**
```bash
docker run -d -p 8000:8000 --name mfukoni-web mfukoni:latest
```

**With data persistence:**
```bash
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  --name mfukoni-web \
  mfukoni:latest
```

**With environment variables:**
```bash
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e DEBUG=False \
  -e SECRET_KEY=your-secret-key \
  -e ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com \
  --name mfukoni-web \
  --restart unless-stopped \
  mfukoni:latest
```

### Container Management

**View logs:**
```bash
docker logs mfukoni-web
docker logs -f mfukoni-web  # Follow logs
```

**Execute commands in container:**
```bash
docker exec -it mfukoni-web bash
docker exec mfukoni-web python migrate_rdbms.py
```

**Stop container:**
```bash
docker stop mfukoni-web
```

**Start stopped container:**
```bash
docker start mfukoni-web
```

**Remove container:**
```bash
docker rm mfukoni-web
```

**Remove container and volume (⚠️ deletes data):**
```bash
docker rm -v mfukoni-web
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `False` | Enable debug mode (set to `True` for development) |
| `SECRET_KEY` | Generated | Django secret key (required for production) |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1,0.0.0.0` | Comma-separated list of allowed hosts |
| `LANGUAGE_CODE` | `en-us` | Language code |
| `TIME_ZONE` | `Africa/Nairobi` | Time zone |

### Security Best Practices

1. **Never commit `.env` file** - It's in `.gitignore`
2. **Use strong SECRET_KEY** in production:
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
3. **Set DEBUG=False** in production
4. **Configure ALLOWED_HOSTS** with your domain
5. **Use HTTPS** in production (requires reverse proxy like nginx)

---

## Data Persistence

### Volume Mounting

The `data/` directory is mounted as a volume to persist the custom RDBMS data:

```yaml
volumes:
  - ./data:/app/data
```

This ensures:
- ✅ Data persists across container restarts
- ✅ Data survives container removal
- ✅ Easy backups by copying the `data/` directory
- ✅ Data can be inspected outside the container

### Backup

**Backup data:**
```bash
tar -czf backup-$(date +%Y%m%d).tar.gz data/
```

**Restore data:**
```bash
tar -xzf backup-YYYYMMDD.tar.gz
```

**Backup from running container:**
```bash
docker exec mfukoni-web tar -czf /tmp/backup.tar.gz /app/data
docker cp mfukoni-web:/tmp/backup.tar.gz ./backup.tar.gz
```

---

## Production Deployment

### Using Docker Compose

1. **Set production environment variables:**
```bash
export DEBUG=False
export SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
export ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

2. **Build and start:**
```bash
docker-compose up -d --build
```

3. **Set up reverse proxy (nginx example):**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

4. **Enable HTTPS** (using Let's Encrypt with certbot):
```bash
sudo certbot --nginx -d yourdomain.com
```

### Using Docker Swarm or Kubernetes

The Docker image is compatible with:
- Docker Swarm
- Kubernetes
- Any container orchestration platform

Example Kubernetes deployment (basic):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mfukoni-web
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mfukoni-web
  template:
    metadata:
      labels:
        app: mfukoni-web
    spec:
      containers:
      - name: web
        image: mfukoni:latest
        ports:
        - containerPort: 8000
        env:
        - name: DEBUG
          value: "False"
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: mfukoni-secrets
              key: secret-key
        volumeMounts:
        - name: data-volume
          mountPath: /app/data
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: mfukoni-data
```

---

## Troubleshooting

### Container won't start

**Check logs:**
```bash
docker logs mfukoni-web
```

**Common issues:**
- Port 8000 already in use → Change port in docker-compose.yml
- Permission denied on data directory → `chmod -R 755 data/`
- Missing environment variables → Check `.env` file

### Can't access the application

1. **Check container is running:**
```bash
docker ps | grep mfukoni
```

2. **Check port mapping:**
```bash
docker port mfukoni-web
```

3. **Check firewall:**
```bash
# Linux
sudo ufw allow 8000

# macOS/Windows - Check firewall settings
```

### Data not persisting

1. **Verify volume mount:**
```bash
docker inspect mfukoni-web | grep Mounts -A 10
```

2. **Check data directory permissions:**
```bash
ls -la data/
chmod -R 755 data/
```

3. **Check if data exists in container:**
```bash
docker exec mfukoni-web ls -la /app/data/mfukoni.db/
```

### RDBMS not initializing

**Manually initialize:**
```bash
docker exec mfukoni-web python migrate_rdbms.py
```

**Check database files:**
```bash
docker exec mfukoni-web ls -la /app/data/mfukoni.db/
```

### Static files not loading

**Collect static files:**
```bash
docker exec mfukoni-web python mfukoni_web/manage.py collectstatic --noinput
```

---

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/)

---

**Questions or Issues?**

Please check the main README.md or open an issue in the project repository.
