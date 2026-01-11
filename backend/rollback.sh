# Rollback function
rollback() {
    error "Deployment failed. Initiating rollback..."
    
    # Stop current containers
    docker-compose down
    
    # Find latest backup
    LATEST_BACKUP=$(ls -t "${BACKUP_DIR}"/backup_*.sql.gz | head -n 1)
    
    if [ -n "$LATEST_BACKUP" ]; then
        log "Restoring from backup: $LATEST_BACKUP"
        
        # Restore database
        gunzip -c "$LATEST_BACKUP" | docker-compose exec -T db psql -U "$DB_USER" "$DB_NAME"
        
        # Restart with previous version (you might need to tag previous image)
        docker-compose up -d
        
        log "Rollback completed"
    else
        error "No backup found for rollback"
    fi
    
    exit 1
}

# Notification
send_notification() {
    STATUS=$1
    MESSAGE=$2
    
    # Send to Slack
    if [ -n "$SLACK_WEBHOOK" ]; then
        curl -X POST "$SLACK_WEBHOOK" \
            -H 'Content-Type: application/json' \
            -d "{\"text\":\"${ENVIRONMENT} Deployment ${STATUS}: ${MESSAGE}\"}"
    fi
    
    # Log notification
    log "Notification sent: $STATUS - $MESSAGE"
}

# Main deployment flow
main() {
    log "Starting deployment to ${ENVIRONMENT}..."
    log "Project directory: ${PROJECT_DIR}"
    
    # Source environment variables
    source "${PROJECT_DIR}/.env"
    
    # Run deployment steps
    pre_deploy_checks || exit 1
    create_backup || exit 1
    pull_images || exit 1
    deploy || { rollback; exit 1; }
    health_check || { rollback; exit 1; }
    smoke_tests || { rollback; exit 1; }
    
    # Success!
    log "✓ Deployment completed successfully!"
    send_notification "SUCCESS" "Deployment to ${ENVIRONMENT} completed"
    
    # Show running containers
    log "Running containers:"
    docker-compose ps
}

# Handle interrupts
trap 'error "Deployment interrupted"; rollback; exit 1' INT TERM

# Run main deployment
main

---
# rollback.sh - Rollback script

#!/bin/bash
set -e

ENVIRONMENT=${1:-production}
PROJECT_DIR="/var/www/dogger-${ENVIRONMENT}"
BACKUP_DIR="${PROJECT_DIR}/backups"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

# List available backups
list_backups() {
    log "Available backups:"
    ls -lh "${BACKUP_DIR}"/backup_*.sql.gz | awk '{print $9, $5, $6, $7, $8}'
}

# Rollback to specific backup
rollback_to_backup() {
    BACKUP_FILE=$1
    
    if [ ! -f "$BACKUP_FILE" ]; then
        error "Backup file not found: $BACKUP_FILE"
        exit 1
    fi
    
    log "Rolling back to: $BACKUP_FILE"
    
    # Stop containers
    cd "$PROJECT_DIR"
    docker-compose down
    
    # Restore database
    log "Restoring database..."
    gunzip -c "$BACKUP_FILE" | docker-compose exec -T db psql -U "$DB_USER" "$DB_NAME"
    
    if [ $? -eq 0 ]; then
        log "Database restored successfully"
    else
        error "Database restoration failed"
        exit 1
    fi
    
    # Restart containers
    docker-compose up -d
    
    # Health check
    sleep 15
    HEALTH_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost/api/health/")
    
    if [ "$HEALTH_CODE" -eq 200 ]; then
        log "✓ Rollback completed successfully!"
    else
        error "Health check failed after rollback"
        exit 1
    fi
}

# Main
if [ "$#" -eq 0 ]; then
    list_backups
    echo ""
    echo "Usage: $0 [environment] <backup_file>"
    echo "Example: $0 production ${BACKUP_DIR}/backup_20240115_120000.sql.gz"
    exit 0
fi

if [ "$#" -eq 2 ]; then
    rollback_to_backup "$2"
else
    # Rollback to latest
    LATEST_BACKUP=$(ls -t "${BACKUP_DIR}"/backup_*.sql.gz | head -n 1)
    rollback_to_backup "$LATEST_BACKUP"
fi