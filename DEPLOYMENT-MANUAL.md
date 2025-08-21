# Alfresco Document Management System - Production Deployment Manual

## Overview

This manual documents the working production deployment of Alfresco Community Edition on the trust server (trustblocks.com). The setup uses Docker Compose with external PostgreSQL database and nginx reverse proxy.

## Architecture

- **Alfresco Repository**: Port 8080 (internal)
- **Alfresco Share**: Port 8081 (internal) 
- **External PostgreSQL**: trust-server-postgres-local container
- **Nginx**: System-level reverse proxy (not containerized)
- **Network**: Docker network "trust-network"

## Prerequisites

1. SSH access to trust server (tmb@trust)
2. Docker and Docker Compose installed
3. External PostgreSQL database running
4. Nginx configured for reverse proxy
5. Git for version control

## Current Working Configuration

### Primary Docker Compose File

Location: `/docker-compose/community-compose.yaml` (working configuration)
Backup: `/docker-compose/community-compose-original.yaml` (original Alfresco version)
Optimized: `/docker-compose/community-compose-optimized.yaml` (enhanced with OCR and Geo Views features)
Minimal: `/docker-compose/minimal-working.yaml` (streamlined version for basic deployment)

Key configuration points:
- Uses external PostgreSQL database `alfresco_prod`
- Memory limits optimized for server (31GB available)
- Hostnames configured for trustblocks.com  
- Connected to trust-network
- Custom application title: "TrustBlocks Document Management"
- NO Traefik proxy (conflicts with nginx)
- Core services only: alfresco, activemq, solr6, transform-core-aio, share

### Critical Environment Variables

```yaml
JAVA_TOOL_OPTIONS: >-
  -Dencryption.keystore.type=JCEKS
  -Dencryption.cipherAlgorithm=DESede/CBC/PKCS5Padding
  -Dencryption.keyAlgorithm=DESede
  -Dencryption.keystore.location=/usr/local/tomcat/shared/classes/alfresco/extension/keystore/keystore
  -Dmetadata-keystore.password=mp6yc0UD9e
  -Dmetadata-keystore.aliases=metadata
  -Dmetadata-keystore.metadata.password=oKIWzVdEdA
  -Dmetadata-keystore.metadata.algorithm=DESede

JAVA_OPTS: >-
  -Ddb.driver=org.postgresql.Driver
  -Ddb.username=postgres
  -Ddb.password=devpassword123
  -Ddb.url=jdbc:postgresql://trust-server-postgres-local:5432/alfresco_prod
  -Dsolr.host=solr6
  -Dsolr.port=8983
  -Dalfresco.host=trustblocks.com
  -Dalfresco.port=80
  -Dshare.host=trustblocks.com
  -Dshare.port=80
```

### Nginx Configuration

Location: `/etc/nginx/sites-available/trustblocks.com`

```nginx
location /alfresco/ {
    proxy_pass http://localhost:8080/alfresco/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

location /share/ {
    proxy_pass http://localhost:8081/share/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## Deployment Steps

### 1. Prepare Environment

```bash
# SSH to server
ssh tmb@trust

# Create deployment directory
mkdir -p /home/tmb/alfresco-production
cd /home/tmb/alfresco-production

# Initialize git repository
git init
git remote add origin https://github.com/Alfresco/acs-deployment.git
```

### 2. Download Official Configuration

```bash
# Clone official Alfresco deployment repository
git clone https://github.com/Alfresco/acs-deployment.git .
```

### 3. Configure Docker Compose

Edit `docker-compose/community-compose.yaml`:

- Update database connection to external PostgreSQL
- Change localhost references to trustblocks.com
- Ensure trust-network configuration
- Verify memory limits for server capacity

### 4. Database Setup

Ensure PostgreSQL database exists:

```bash
# Connect to postgres container
docker exec -it trust-server-postgres-local psql -U postgres

# Create production database
CREATE DATABASE alfresco_prod;
\q
```

### 5. Network Setup

```bash
# Create external docker network if not exists
docker network create trust-network
```

### 6. Deploy Services

```bash
cd /home/tmb/alfresco-production/docker-compose
docker compose -f community-compose.yaml up -d
```

### 7. Verify Deployment

Check service status:
```bash
docker compose -f community-compose.yaml ps
docker compose -f community-compose.yaml logs
```

Access points:
- Internal: http://localhost:8080/alfresco and http://localhost:8081/share
- External: http://trustblocks.com/alfresco and http://trustblocks.com/share

## Troubleshooting

### Common Issues

1. **"Cannot find Alfresco Repository" error**
   - Ensure JAVA_TOOL_OPTIONS includes encryption settings
   - Verify database connection parameters
   - Check that alfresco service is healthy before share starts

2. **Port conflicts**
   - Stop old/conflicting containers
   - Ensure no other services using ports 8080/8081

3. **Database connection issues**
   - Verify PostgreSQL container is running
   - Check network connectivity between containers
   - Confirm database credentials

4. **External access issues**
   - Verify nginx configuration and restart: `sudo systemctl restart nginx`
   - Check hostname configuration in JAVA_OPTS
   - Ensure proxy headers are set correctly

### Service Commands

**IMPORTANT**: Start only core services to avoid Traefik proxy conflicts:

```bash
# Start core services (RECOMMENDED)
docker compose -f community-compose.yaml up -d alfresco activemq solr6 transform-core-aio share

# Stop services
docker compose -f community-compose.yaml down

# View logs
docker compose -f community-compose.yaml logs -f [service_name]

# Restart specific service
docker compose -f community-compose.yaml restart [service_name]

# Check service status
docker compose -f community-compose.yaml ps
```

## Backup and Restore

### Content Store Backup
Content is stored in Docker volume `alf_data`. Backup using:
```bash
docker run --rm -v alf_data:/data -v /backup:/backup alpine tar czf /backup/alf_data.tar.gz -C /data .
```

### Database Backup
```bash
docker exec trust-server-postgres-local pg_dump -U postgres alfresco_prod > alfresco_backup.sql
```

### Restore Process
1. Stop Alfresco services
2. Restore database from dump
3. Restore content store from backup
4. Start services

## Maintenance

### Regular Tasks
- Monitor disk space for Docker volumes
- Monitor PostgreSQL database size
- Check logs for errors
- Update container images as needed

### Version Updates
- Update image tags in docker-compose.yaml
- Test in development environment first
- Backup before production updates

## Security Notes

- Database credentials are in environment variables
- Encryption keys are embedded in configuration
- External access requires nginx security headers
- Consider SSL/TLS termination at nginx level

## File Locations

- Docker Compose: `/home/tmb/alfresco-production/docker-compose/community-compose.yaml`
- Nginx Config: `/etc/nginx/sites-available/trustblocks.com`
- PostgreSQL: External container `trust-server-postgres-local`
- Content Store: Docker volume `alf_data`
- Git Repository: `/home/tmb/alfresco-production`
- MCP Server: `/home/tmb/alfresco/python-alfresco-mcp-server`

## Support Information

- Official Documentation: https://alfresco.github.io/acs-deployment/
- Community Forum: https://hub.alfresco.com
- Issue Tracking: Git repository for configuration changes