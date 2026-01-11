#!/bin/bash
# quick-setup.sh - Automated CI/CD setup script for Dogger 2.0

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Banner
echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        🚀 Dogger 2.0 CI/CD Quick Setup 🚀                 ║
║                                                           ║
║     Automated setup for production deployment             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Helper functions
print_step() {
    echo -e "${GREEN}[STEP]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_step "Checking prerequisites..."
    
    local missing=0
    
    # Check Git
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed"
        missing=1
    else
        print_info "✓ Git found: $(git --version)"
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        missing=1
    else
        print_info "✓ Docker found: $(docker --version)"
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        missing=1
    else
        print_info "✓ Docker Compose found: $(docker-compose --version)"
    fi
    
    if [ $missing -eq 1 ]; then
        print_error "Missing prerequisites. Please install missing tools."
        exit 1
    fi
    
    echo ""
}

# Collect information
collect_info() {
    print_step "Collecting deployment information..."
    echo ""
    
    # GitHub info
    read -p "GitHub username: " GITHUB_USER
    read -p "Repository name (default: dogger-2.0): " REPO_NAME
    REPO_NAME=${REPO_NAME:-dogger-2.0}
    
    # Server info
    read -p "Production server IP/hostname: " PROD_HOST
    read -p "Production SSH user (default: deploy): " PROD_USER
    PROD_USER=${PROD_USER:-deploy}
    
    read -p "Staging server IP/hostname (press Enter to skip): " STAGING_HOST
    if [ -n "$STAGING_HOST" ]; then
        read -p "Staging SSH user (default: deploy): " STAGING_USER
        STAGING_USER=${STAGING_USER:-deploy}
    fi
    
    # Domain info
    read -p "Production domain (e.g., dogger.example.com): " PROD_DOMAIN
    
    # Slack webhook (optional)
    read -p "Slack webhook URL (press Enter to skip): " SLACK_WEBHOOK
    
    # Database credentials
    print_info "Database configuration:"
    read -p "Database name (default: dogger_prod): " DB_NAME
    DB_NAME=${DB_NAME:-dogger_prod}
    read -p "Database user (default: dogger): " DB_USER
    DB_USER=${DB_USER:-dogger}
    read -sp "Database password: " DB_PASSWORD
    echo ""
    
    # Redis password
    read -sp "Redis password: " REDIS_PASSWORD
    echo ""
    
    # Django secret key
    SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
    
    echo ""
    print_info "Configuration collected successfully!"
    echo ""
}

# Create GitHub repository
setup_github() {
    print_step "Setting up GitHub repository..."
    
    # Initialize git if not already
    if [ ! -d .git ]; then
        git init
        git branch -M main
    fi
    
    # Create .gitignore if doesn't exist
    if [ ! -f .gitignore ]; then
        cat > .gitignore << 'EOF'
*.pyc
__pycache__/
*.sqlite3
.env
.env.*
!.env.example
staticfiles/
mediafiles/
logs/
*.log
.DS_Store
.vscode/
.idea/
EOF
    fi
    
    # Add remote if not exists
    if ! git remote | grep -q origin; then
        git remote add origin "https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
    fi
    
    print_info "✓ Git repository configured"
}

# Create GitHub Actions workflow
create_workflow() {
    print_step "Creating GitHub Actions workflow..."
    
    mkdir -p .github/workflows
    
    # Copy the workflow file (you'll need to manually copy the YAML content)
    print_warning "Please copy the GitHub Actions workflow to: .github/workflows/cicd.yml"
    print_info "The workflow file is provided in the artifacts."
    
    echo ""
}

# Create Docker files
create_docker_files() {
    print_step "Creating Docker configuration..."
    
    # Create Dockerfile (copy from artifact)
    print_warning "Please copy the Dockerfile to: backend/Dockerfile"
    
    # Create docker-compose.yml
    cat > docker-compose.yml << EOF
version: '3.9'

services:
  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data

  web:
    build: ./backend
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
      - ALLOWED_HOSTS=${PROD_DOMAIN}
    depends_on:
      - db
      - redis
    ports:
      - "8000:8000"

volumes:
  postgres_data:
  redis_data:
EOF
    
    print_info "✓ Docker files created"
}

# Create environment file
create_env_file() {
    print_step "Creating environment template..."
    
    cat > .env.example << EOF
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=${PROD_DOMAIN}
DJANGO_SETTINGS_MODULE=dogger.settings.production

# Database
DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_PASSWORD=your-database-password
DATABASE_URL=postgresql://${DB_USER}:password@db:5432/${DB_NAME}

# Redis
REDIS_PASSWORD=your-redis-password
REDIS_URL=redis://:password@redis:6379/0

# CORS
CORS_ALLOWED_ORIGINS=https://${PROD_DOMAIN}

# Monitoring
GRAFANA_USER=admin
GRAFANA_PASSWORD=your-grafana-password

# GitHub
GITHUB_REPOSITORY=${GITHUB_USER}/${REPO_NAME}
EOF
    
    print_info "✓ Environment template created"
}

# Generate SSH key
generate_ssh_key() {
    print_step "Generating SSH deployment key..."
    
    if [ ! -f ~/.ssh/dogger_deploy ]; then
        ssh-keygen -t ed25519 -f ~/.ssh/dogger_deploy -N "" -C "dogger-deploy-key"
        print_info "✓ SSH key generated: ~/.ssh/dogger_deploy"
        echo ""
        print_warning "Add this public key to your server's authorized_keys:"
        cat ~/.ssh/dogger_deploy.pub
        echo ""
        read -p "Press Enter when you've added the key to your server..."
    else
        print_info "SSH key already exists"
    fi
}

# Create deployment instructions
create_instructions() {
    print_step "Creating setup instructions..."
    
    cat > SETUP_INSTRUCTIONS.md << EOF
# Dogger 2.0 Deployment Setup

## GitHub Secrets Required

Add these secrets to your GitHub repository (Settings → Secrets → Actions):

\`\`\`
PROD_HOST=${PROD_HOST}
PROD_USER=${PROD_USER}
PROD_SSH_KEY=<contents of ~/.ssh/dogger_deploy>
EOF

    if [ -n "$STAGING_HOST" ]; then
        cat >> SETUP_INSTRUCTIONS.md << EOF
STAGING_HOST=${STAGING_HOST}
STAGING_USER=${STAGING_USER}
STAGING_SSH_KEY=<contents of ~/.ssh/dogger_deploy>
EOF
    fi

    if [ -n "$SLACK_WEBHOOK" ]; then
        cat >> SETUP_INSTRUCTIONS.md << EOF
SLACK_WEBHOOK=${SLACK_WEBHOOK}
EOF
    fi

    cat >> SETUP_INSTRUCTIONS.md << 'EOF'
```

## Server Setup Commands

Run these commands on your production server:

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create deploy user
sudo useradd -m -s /bin/bash deploy
sudo usermod -aG docker deploy

# Create project directory
sudo mkdir -p /var/www/dogger-prod
sudo chown deploy:deploy /var/www/dogger-prod

# Setup SSH
sudo -u deploy mkdir -p /home/deploy/.ssh
# Add your public key to /home/deploy/.ssh/authorized_keys
```

## Next Steps

1. Add GitHub secrets
2. Setup production server
3. Push code to GitHub: `git push origin main`
4. Monitor deployment in GitHub Actions

## Manual Deployment

```bash
# SSH to server
ssh deploy@your-server

# Clone repository
cd /var/www/dogger-prod
git clone https://github.com/YOUR_USERNAME/dogger-2.0.git .

# Copy environment file
cp .env.example .env
# Edit .env with actual values

# Start services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```
EOF
    
    print_info "✓ Setup instructions created: SETUP_INSTRUCTIONS.md"
}

# Summary
print_summary() {
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                           ║${NC}"
    echo -e "${GREEN}║              ✓ Setup Complete!                            ║${NC}"
    echo -e "${GREEN}║                                                           ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    echo -e "${BLUE}Next Steps:${NC}"
    echo ""
    echo "1. Review SETUP_INSTRUCTIONS.md for detailed setup"
    echo "2. Add GitHub secrets (see SETUP_INSTRUCTIONS.md)"
    echo "3. Copy workflow files from artifacts to .github/workflows/"
    echo "4. Setup production server"
    echo "5. Push to GitHub:"
    echo "   git add ."
    echo "   git commit -m 'Setup CI/CD pipeline'"
    echo "   git push origin main"
    echo ""
    
    echo -e "${YELLOW}Important Files Created:${NC}"
    echo "  - docker-compose.yml (production)"
    echo "  - .env.example (environment template)"
    echo "  - SETUP_INSTRUCTIONS.md (deployment guide)"
    echo "  - .github/workflows/ (to be created)"
    echo ""
    
    echo -e "${YELLOW}SSH Key Location:${NC}"
    echo "  - Private: ~/.ssh/dogger_deploy"
    echo "  - Public: ~/.ssh/dogger_deploy.pub"
    echo ""
    
    print_info "Good luck with your deployment! 🚀"
}

# Main execution
main() {
    clear
    
    check_prerequisites
    collect_info
    setup_github
    create_workflow
    create_docker_files
    create_env_file
    generate_ssh_key
    create_instructions
    print_summary
}

# Run main function
main