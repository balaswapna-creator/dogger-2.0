#!/bin/bash
# deploy.sh - Main deployment script

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-production}
PROJECT_DIR="/var/www/dogger-${ENVIRONMENT}"
BACKUP_DIR="${PROJECT_DIR}/backups"
LOG_FILE="${PROJECT_DIR}/logs/deploy-$(date +%Y%m%d_%H%M%S).log"

# Functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1" | tee -a "$LOG_FILE"
}

# Pre-deployment checks
pre_deploy_checks() {
    log "Running pre-deployment checks..."
    
    # Check if docker is running
    if ! docker info > /dev/null 2>&1; then
        error "Docker is not running"
        exit 1
    fi
    
    # Check disk space (require at least 5GB free)
    FREE_SPACE=$(df -BG "${PROJECT_DIR}" | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ "$FREE_SPACE" -lt 5 ]; then
        error "Insufficient disk space. Free space: ${FREE_SPACE}GB"
        exit 1
    fi
    
    # Check environment file exists
    if [ ! -f "${PROJECT_DIR}/.env" ]; then
        error "Environment file not found: ${PROJECT_DIR}/.env"
        exit 1
    fi
    
    log "Pre-deployment checks passed ✓"
}

# Create backup
create_backup() {
    log "Creating backup..."
    
    mkdir -p "$BACKUP_DIR"
    BACKUP_NAME="backup_$(date +%Y%m%d_%H%M%S)"
    
    # Backup database
    docker-compose -f "${PROJECT_DIR}/docker-compose.yml" exec -T db \
        pg_dump -U "$DB_USER" "$DB_NAME" > "${BACKUP_DIR}/${BACKUP_NAME}.sql"
    
    if [ $? -eq 0 ]; then
        log "Database backup created: ${BACKUP_NAME}.sql"
        
        # Compress backup
        gzip "${BACKUP_DIR}/${BACKUP_NAME}.sql"
        
        # Keep only last 7 backups
        cd "$BACKUP_DIR"
        ls -t backup_*.sql.gz | tail -n +8 | xargs -r rm
        
        # Save current docker image tag
        docker-compose -f "${PROJECT_DIR}/docker-compose.yml" images > "${BACKUP_DIR}/${BACKUP_NAME}.images"
        
        log "Backup completed successfully ✓"
    else
        error "Database backup failed"
        exit 1
    fi
}

# Pull latest images
pull_images() {
    log "Pulling latest Docker images..."
    
    cd "$PROJECT_DIR"
    docker-compose pull
    
    if [ $? -eq 0 ]; then
        log "Images pulled successfully ✓"
    else
        error "Failed to pull images"
        exit 1
    fi
}

# Deploy application
deploy() {
    log "Deploying application..."
    
    cd "$PROJECT_DIR"
    
    # Start services
    docker-compose up -d
    
    if [ $? -ne 0 ]; then
        error "Failed to start services"
        exit 1
    fi
    
    # Wait for services to be healthy
    log "Waiting for services to be healthy..."
    sleep 10
    
    # Run migrations
    log "Running database migrations..."
    docker-compose exec -T web python manage.py migrate --noinput
    
    if [ $? -ne 0 ]; then
        error "Database migration failed"
        return 1
    fi
    
    # Collect static files
    log "Collecting static files..."
    docker-compose exec -T web python manage.py collectstatic --noinput
    
    # Clear cache
    log "Clearing cache..."
    docker-compose exec -T web python manage.py clear_cache || true
    
    log "Deployment completed ✓"
}

# Health check
health_check() {
    log "Running health checks..."
    
    # Wait for application to start
    sleep 15
    
    # Check application health endpoint
    HEALTH_URL="http://localhost/api/health/"
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$HEALTH_URL")
    
    if [ "$HTTP_CODE" -eq 200 ]; then
        log "Health check passed ✓ (HTTP $HTTP_CODE)"
        return 0
    else
        error "Health check failed (HTTP $HTTP_CODE)"
        return 1
    fi
}

# Smoke tests
smoke_tests() {
    log "Running smoke tests..."
    
    # Test authentication endpoint
    AUTH_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost/api/auth/register/")
    if [ "$AUTH_CODE" -ne 405 ] && [ "$AUTH_CODE" -ne 200 ]; then
        warning "Auth endpoint returned unexpected code: $AUTH_CODE"
    fi
    
    # Test database connectivity
    docker-compose exec -T db pg_isready -U "$DB_USER" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        log "Database connectivity test passed ✓"
    else
        error "Database connectivity test failed"
        return 1
    fi
    
    # Test Redis connectivity
    docker-compose exec -T redis redis-cli ping > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        log "Redis connectivity test passed ✓"
    else
        error "Redis connectivity test failed"
        return 1
    fi
    
    log "All smoke tests passed ✓"
    return 0
}
