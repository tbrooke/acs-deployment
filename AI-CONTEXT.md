# Alfresco Production Deployment - AI Assistant Context Document

## Purpose
This document provides context for AI assistants (Claude, ChatGPT, etc.) to understand and recreate the Alfresco Document Management System deployment on the trust server. Use this for troubleshooting, maintenance, and automation with tools like Babashka or Puppet.

## Server Environment
- **Hostname**: trust server (trustblocks.com)
- **SSH Access**: tmb@trust (password: tmb)
- **OS**: Linux server with Docker
- **Memory**: 31GB available
- **Network**: Docker network "trust-network"

## Architecture Overview
```
Internet → Nginx (system-level) → Docker Containers
                ↓
    ┌─────────────────┬─────────────────┐
    │ Alfresco:8080   │ Share:8081      │
    └─────────────────┴─────────────────┘
                ↓
    External PostgreSQL Container
    (trust-server-postgres-local)
```

## Key Decisions Made
1. **Removed Traefik**: Conflicted with nginx, simplified to nginx-only
2. **External PostgreSQL**: Used existing container for centralized database management
3. **Fresh Install**: Started clean rather than fixing broken configuration
4. **Minimal Changes**: Success came from keeping close to official configuration
5. **Production Database**: Created `alfresco_prod` instead of `alfresco_dev`

## Critical Configuration Files

### Primary Docker Compose
**Location**: `/home/tmb/alfresco-production/docker-compose/community-compose.yaml` (WORKING CONFIG)
**Backup**: `/home/tmb/alfresco-production/docker-compose/community-compose-original.yaml`
**Optimized**: `/home/tmb/alfresco-production/docker-compose/community-compose-optimized.yaml` (Enhanced with OCR/Geo features)
**Minimal**: `/home/tmb/alfresco-production/docker-compose/minimal-working.yaml` (Streamlined version)

**Key Changes from Official**:
- Database URL: `jdbc:postgresql://trust-server-postgres-local:5432/alfresco_prod`
- Hostnames: localhost → trustblocks.com (lines 30-35, 88-89)
- Network: Uses external "trust-network"
- Memory: Optimized for server (3GB alfresco, 1GB share, etc.)
- Application title: "TrustBlocks Document Management"
- **CRITICAL**: Removed Traefik proxy service (conflicts with nginx on port 8080)

**Critical Environment Variables** (DO NOT REMOVE):
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
```

### Nginx Configuration
**Location**: `/etc/nginx/sites-available/trustblocks.com`

Routes `/alfresco/` to `localhost:8080` and `/share/` to `localhost:8081` with proper proxy headers.

### External Database
**Container**: `trust-server-postgres-local`
**Database**: `alfresco_prod`
**Location**: `/home/tmb/database/docker-compose.yml`

## Working State Verification
1. `docker compose -f community-compose.yaml ps` - all services UP
2. `http://localhost:8080/alfresco` - internal repository access
3. `http://localhost:8081/share` - internal share access  
4. `http://trustblocks.com/alfresco` - external access
5. `http://trustblocks.com/share` - external share access

## Common Failure Patterns
1. **"Cannot find Alfresco Repository"** - Missing JAVA_TOOL_OPTIONS encryption settings
2. **Port conflicts** - Other services binding to 8080/8081
3. **Database connection** - PostgreSQL container not running or wrong network
4. **localhost redirects** - Hostname configuration in JAVA_OPTS incorrect

## Deployment Commands
```bash
# SSH to server
ssh tmb@trust

# Navigate to deployment
cd /home/tmb/alfresco-production/docker-compose

# Deploy CORE SERVICES ONLY (avoids Traefik conflicts)
docker compose -f community-compose.yaml up -d alfresco activemq solr6 transform-core-aio share

# Monitor
docker compose -f community-compose.yaml logs -f

# Stop
docker compose -f community-compose.yaml down
```

## Backup Locations (for restoration)
- Content store backups: Look for tar/zip archives
- Database dumps: Look for .sql files
- Previous working configurations in git history

## For Automation (Babashka/Puppet)
1. **Infrastructure**: Ensure Docker, networks, external PostgreSQL
2. **Configuration Management**: Template the docker-compose.yaml
3. **Secrets Management**: Handle database credentials securely  
4. **Health Checks**: Monitor service startup and connectivity
5. **Backup Automation**: Schedule content store and database backups

## Network Dependencies
- **trust-network**: Must exist before deployment
- **PostgreSQL**: External container must be running and accessible
- **nginx**: System service must be configured and running

## Service Startup Order
1. PostgreSQL (external - already running)
2. ActiveMQ, Solr6, Transform services
3. Alfresco repository (waits for dependencies)
4. Share (waits for healthy alfresco)

## Troubleshooting Quick Reference
- **Logs**: `docker compose -f community-compose.yaml logs [service]`
- **Health**: `docker compose -f community-compose.yaml ps`
- **Database**: `docker exec -it trust-server-postgres-local psql -U postgres`
- **Network**: `docker network ls` and `docker network inspect trust-network`
- **Nginx**: `sudo systemctl status nginx` and `sudo nginx -t`

## Git Repository
- **Location**: `/home/tmb/alfresco-production`
- **Remote**: https://github.com/tbrooke/acs-deployment.git
- **Branch**: production
- **Purpose**: Version control for configuration changes and rollback capability

## Additional Context
- **MCP Server**: Python Alfresco MCP server installed at `/home/tmb/alfresco/python-alfresco-mcp-server`
- **Directory Structure**: Reorganized with deployment at `~/alfresco/alfresco-production` and MCP server separately
- **Configuration Files**: Multiple variants including optimized (with OCR/Geo features) and minimal working configs

## Success Indicators
- All containers show "UP" status
- Alfresco repository responds to health check
- External access works through nginx
- No "Cannot find repository" errors
- Database connections established

## Future Automation Considerations
- Template hostnames for different environments
- Externalize database credentials
- Add SSL/TLS termination
- Implement proper logging and monitoring
- Add automated backup scheduling
- Consider container orchestration (Docker Swarm/K8s) for scaling