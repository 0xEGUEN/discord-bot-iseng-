#!/bin/bash
# Discord Bot Startup Script for Pterodactyl Panel
# This script is designed to run in Pterodactyl Panel environments

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  DISCORD BOT - PTERODACTYL PANEL ${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Set working directory
cd "$(dirname "$0")" || exit 1

# Function to print colored output
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if .env file exists
log_info "Checking .env file..."
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        log_warning ".env not found, copying from .env.example"
        cp .env.example .env
        log_success ".env created - PLEASE EDIT WITH YOUR TOKEN"
    else
        log_error ".env file not found!"
        exit 1
    fi
else
    log_success ".env file exists"
fi

# Check if requirements.txt exists
log_info "Checking requirements.txt..."
if [ ! -f requirements.txt ]; then
    log_error "requirements.txt not found!"
    exit 1
fi
log_success "requirements.txt found"

# Find Python executable
log_info "Finding Python installation..."
PYTHON_CMD=""

if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    log_error "Python not found!"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
log_success "Python found: $PYTHON_VERSION"

# Install/Update dependencies with retry logic
log_info "Installing Python dependencies (this may take a few minutes)..."
RETRY_COUNT=0
MAX_RETRIES=3

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    $PYTHON_CMD -m pip install --upgrade pip setuptools wheel -q 2>/dev/null
    $PYTHON_CMD -m pip install -r requirements.txt --upgrade 2>&1 | grep -E "(Successfully|Requirement|ERROR|error)" | tail -5
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        log_success "Dependencies installed successfully"
        break
    else
        RETRY_COUNT=$((RETRY_COUNT + 1))
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            log_warning "Installation failed, retrying... ($RETRY_COUNT/$MAX_RETRIES)"
            sleep 5
        else
            log_error "Failed to install dependencies after $MAX_RETRIES attempts"
        fi
    fi
done

# Final checks
log_info "Running final checks..."
if [ ! -f bot.py ]; then
    log_error "bot.py not found!"
    exit 1
fi
log_success "bot.py found"

# Check for DISCORD_TOKEN
if [ -z "$DISCORD_TOKEN" ]; then
    if grep -q "DISCORD_TOKEN=" .env; then
        log_warning "DISCORD_TOKEN is in .env file"
    else
        log_error "DISCORD_TOKEN not found in .env!"
        log_info "Please set DISCORD_TOKEN in environment variables or .env file"
        exit 1
    fi
fi
log_success "DISCORD_TOKEN is configured"

# Check FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    log_warning "FFmpeg not found - music features may not work"
    log_info "Install FFmpeg: apt-get install ffmpeg"
fi

# Start the bot and web server
echo ""
log_info "Starting Discord Bot and Web Server..."
log_info "======================================="

# Check if web app exists
if [ -f web/app.py ]; then
    log_info "Starting Web Server on port 5000..."
    # Set HOST=0.0.0.0 untuk Pterodactyl Panel agar accessible dari network
    HOST=0.0.0.0 PORT=5000 $PYTHON_CMD web/app.py >> bot.log 2>&1 &
    WEB_PID=$!
    log_success "Web Server started (PID: $WEB_PID)"
    log_info "Dashboard available at http://0.0.0.0:5000"
    echo ""
else
    log_warning "web/app.py not found - skipping web server"
fi

# Set trap to cleanup web server on exit
trap 'kill $WEB_PID 2>/dev/null' EXIT

log_info "Starting Discord Bot..."
log_info "Bot will log to: bot.log"

# Execute bot.py with Python (foreground for Pterodactyl)
$PYTHON_CMD bot.py
