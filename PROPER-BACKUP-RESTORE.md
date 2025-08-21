# Alfresco Proper Backup and Restore Procedure

## Why Our Previous Backup Failed

Alfresco has **three interconnected components** that must be backed up and restored as a synchronized set:

1. **PostgreSQL Database** - Metadata and transactions
2. **Content Store** - Actual files on disk  
3. **Solr Indexes** - Search indexes

**Our mistake**: We only backed up database + content store, missing Solr indexes entirely.

## Official Backup Order (CRITICAL)

### Backup Order (Forward):
1. **First**: Solr indexes (`solr6Backup`)
2. **Second**: Database dump
3. **Third**: Content store files

### Restore Order (Reverse):
1. **First**: Content store files
2. **Second**: Database restore
3. **Third**: Solr indexes (or allow full reindex)

## Correct Backup Procedure

### Step 1: Stop All Services (Cold Backup)
```bash
cd /home/tmb/alfresco-fresh-git/docker-compose
docker compose -f community-compose.yaml down
```

### Step 2: Backup Solr Indexes
```bash
# Create backup directory with timestamp
BACKUP_DIR="/home/tmb/alfresco-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p $BACKUP_DIR

# Backup Solr data volume
docker run --rm -v solr_data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/solr_indexes.tar.gz -C /data .
```

### Step 3: Backup Database  
```bash
docker exec trust-server-postgres-local pg_dump -U postgres alfresco_prod > $BACKUP_DIR/database.dump
```

### Step 4: Backup Content Store
```bash
docker run --rm -v alf_data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/contentstore.tar.gz -C /data .
```

### Step 5: Create Backup Manifest
```bash
cat > $BACKUP_DIR/backup-info.txt << EOF
Backup created: $(date)
Alfresco version: 25.2.0
Database: alfresco_prod
Components:
- solr_indexes.tar.gz (Solr search indexes)
- database.dump (PostgreSQL database)
- contentstore.tar.gz (Document files)

Restore order:
1. contentstore.tar.gz
2. database.dump  
3. solr_indexes.tar.gz (or reindex)
EOF
```

## Correct Restore Procedure

### Step 1: Stop Services
```bash
cd /home/tmb/alfresco-fresh-git/docker-compose
docker compose -f community-compose.yaml down
```

### Step 2: Clean Existing Data
```bash
# Clean database
docker exec trust-server-postgres-local dropdb -U postgres alfresco_prod
docker exec trust-server-postgres-local createdb -U postgres alfresco_prod

# Clean volumes
docker volume rm alf_data solr_data
docker volume create alf_data
docker volume create solr_data
```

### Step 3: Restore Content Store (First)
```bash
BACKUP_DIR="/path/to/your/backup"
docker run --rm -v alf_data:/data -v $BACKUP_DIR:/backup alpine tar xzf /backup/contentstore.tar.gz -C /data
```

### Step 4: Restore Database (Second)
```bash
docker exec -i trust-server-postgres-local psql -U postgres -d alfresco_prod < $BACKUP_DIR/database.dump
```

### Step 5: Restore Solr Indexes (Third) - OPTIONAL
```bash
# Option A: Restore indexes (faster startup)
docker run --rm -v solr_data:/data -v $BACKUP_DIR:/backup alpine tar xzf /backup/solr_indexes.tar.gz -C /data

# Option B: Let Alfresco rebuild indexes (safer, slower)
# Skip this step and Alfresco will automatically reindex on first startup
```

### Step 6: Start Services and Monitor
```bash
docker compose -f community-compose.yaml up -d alfresco activemq solr6 transform-core-aio share

# Monitor startup logs
docker compose -f community-compose.yaml logs -f alfresco | grep -i "error\|content integrity"
docker compose -f community-compose.yaml logs -f solr6 | grep -i "reindex"
```

## Troubleshooting Restored System

### If Alfresco Still Unhealthy After Restore:

1. **Check content integrity errors**:
   ```bash
   docker compose -f community-compose.yaml logs alfresco | grep -i "content integrity"
   ```

2. **Force full Solr reindex** (if needed):
   ```bash
   # Stop services
   docker compose -f community-compose.yaml down
   
   # Clear Solr indexes
   docker volume rm solr_data
   docker volume create solr_data
   
   # Restart - Alfresco will rebuild indexes
   docker compose -f community-compose.yaml up -d alfresco activemq solr6 transform-core-aio share
   ```

3. **Check for cluster ID conflicts** (if cloning):
   - Look for `cluster.id` in database or config
   - Clear it when creating test/dev copies

## Why This Approach Works

- **Consistency**: All three components from same point in time
- **Proper ordering**: Prevents missing node references  
- **Cold backup**: No live changes during backup
- **Index flexibility**: Can restore indexes or rebuild them

## Quick Test Validation

After restore, verify:
```bash
# Check all services healthy
docker compose -f community-compose.yaml ps

# Test document access
curl http://localhost:8080/alfresco/

# Test Share access  
curl http://localhost:8081/share/

# Check external access
curl http://trustblocks.com/alfresco/
curl http://trustblocks.com/share/
```

## Current Status: BACKUP/RESTORE NEEDS FURTHER RESEARCH

### Testing Results (Aug 21, 2025)
- ✅ **Backup procedure works**: All 3 components backed up successfully
- ❌ **Restore procedure fails**: Even with proper 3-component restore, Alfresco fails to start
- ❌ **Issue persists**: Same startup errors regardless of Solr index approach
- 🔍 **Root cause**: Appears to be database compatibility issues, not just missing Solr indexes

### Error Pattern
Restored databases consistently cause Alfresco startup failures with Quartz scheduler errors, suggesting configuration incompatibilities between backed-up state and current setup.

### Recommendations
1. **For now**: Use working clean system and recreate content manually
2. **Future**: Investigate BART (Backup and Recovery Tool) modernization for Docker
3. **Alternative**: Focus on export/import of individual documents rather than full system restore
4. **Backup**: Keep configuration files and deployment documentation in git

### Working System
The current clean installation works perfectly:
- Fresh database initialization
- Docker-based deployment  
- External nginx proxy
- External PostgreSQL database
- Version controlled configuration

## Backup Schedule Recommendation (For Configuration Only)

- **Daily**: Git commits of configuration changes
- **Before changes**: Manual backup before system updates  
- **Documentation**: Keep deployment procedures current
- **Content**: Plan for manual recreation rather than automated restore