#!/bin/bash

# WSERVER="./wserver.sh"
# VARS_PATH="./deploy-vars.sh"


# # update packages
# apt update
# apt-get update -y

# # install git
# apt install git
# git config --global user.name "nikolav"
# git config --global user.email "admin@nikolav.rs"


# # install docker
# apt-get remove docker docker-engine docker.io containerd runc
# apt-get update
# apt-get install -y ca-certificates curl gnupg lsb-release
# mkdir -p /etc/apt/keyrings
# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
# echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
# apt-get update
# apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# # install docker-compose
# curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
# chmod +x /usr/local/bin/docker-compose

# Install Docker
# apt-get remove -y docker docker-engine docker.io containerd runc
# apt-get update
# apt-get install -y ca-certificates curl gnupg lsb-release

# # Add Docker's official GPG key
# mkdir -p /etc/apt/keyrings
# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# # Set up the stable repository
# echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# # Install Docker Engine
# apt-get update
# apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# # (Optional) Enable docker-compose alias for backwards compatibility
# update-alternatives --install /usr/local/bin/docker-compose docker-compose /usr/libexec/docker/cli-plugins/docker-compose 1

# # allow app @ports
# ufw allow OpenSSH
# ufw allow http
# ufw allow https
# ufw allow 'Nginx Full'
# # endpoint:app
# ufw allow 5000
# ufw enable

# # set env variables
# if [ -f "$VARS_PATH" ]; then
#   source "$VARS_PATH"
# fi

# #  exe server script
# if [ -e "$WSERVER" ]; then
#   chmod 755 $WSERVER
# fi

# # shortcuts
# alias ll='ls -AlFht --color=auto --group-directories-first '
# alias gs='git status '

# # status check
# echo '== status'
# git --version
# docker --version
# docker compose version
# service docker status
# ufw status verbose




##################################################################
##################################################################
# Improved Web Development Server Setup Script with Docker Support

# --- Configuration Section ---
WSERVER="./wserver.sh"
VARS_PATH="./deploy-vars.sh"
LOG_FILE="./server_setup.log"
DOCKER_COMPOSE_VERSION="v2.27.0"  # Latest stable version
USERNAME=$(whoami)

# --- Helper Functions ---
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# check_command() {
#     if ! command -v $1 &> /dev/null; then
#         log_message "ERROR: $1 could not be found"
#         exit 1
#     fi
# }

# --- Initial Setup ---
log_message "Starting server setup process"

# Update system packages
log_message "Updating package lists..."
apt-get update -y | tee -a $LOG_FILE
apt-get upgrade -y | tee -a $LOG_FILE

# Install essential tools
log_message "Installing essential packages..."
apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    software-properties-common \
    apt-transport-https \
    htop \
    net-tools \
    ufw \
    fail2ban \
    unattended-upgrades \
    git \
    jq \
    make \
    nginx \
    python3-pip | tee -a $LOG_FILE

# --- Docker Installation ---
log_message "Installing Docker..."

# Remove old versions
apt-get remove -y docker docker-engine docker.io containerd runc | tee -a $LOG_FILE

# Set up Docker repository
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker components
apt-get update -y | tee -a $LOG_FILE
apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin | tee -a $LOG_FILE

# Install specific docker-compose version
log_message "Installing Docker Compose $DOCKER_COMPOSE_VERSION..."
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL "https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose

# Configure Docker to start on boot
systemctl enable docker.service | tee -a $LOG_FILE
systemctl enable containerd.service | tee -a $LOG_FILE

# Add current user to docker group (to run without sudo)
usermod -aG docker $USERNAME | tee -a $LOG_FILE

# --- Security Setup ---
log_message "Configuring security settings..."

# Configure UFW firewall
ufw allow OpenSSH | tee -a $LOG_FILE
ufw allow http | tee -a $LOG_FILE
ufw allow https | tee -a $LOG_FILE
ufw allow 'Nginx Full' | tee -a $LOG_FILE
ufw allow 5000/tcp | tee -a $LOG_FILE
ufw --force enable | tee -a $LOG_FILE

# Configure fail2ban
# systemctl enable fail2ban | tee -a $LOG_FILE
# systemctl start fail2ban | tee -a $LOG_FILE

# Configure automatic security updates
echo 'Unattended-Upgrade::Automatic-Reboot "true";' > /etc/apt/apt.conf.d/50unattended-upgrades
echo 'Unattended-Upgrade::Mail "admin@nikolav.rs";' >> /etc/apt/apt.conf.d/50unattended-upgrades
echo 'Unattended-Upgrade::Automatic-Reboot-Time "03:33";' >> /etc/apt/apt.conf.d/50unattended-upgrades

# --- Environment Configuration ---
# Load variables if exists
if [ -f "$VARS_PATH" ]; then
    log_message "Loading environment variables from $VARS_PATH"
    source "$VARS_PATH"
fi

# Make server script executable if exists
if [ -e "$WSERVER" ]; then
    log_message "Making $WSERVER executable"
    chmod 755 $WSERVER
fi

# --- Post-Installation Checks ---
log_message "Running post-installation checks..."

# Verify installations
# check_command git
# check_command docker
# check_command docker-compose

# Docker health check
# docker run hello-world | tee -a $LOG_FILE

# --- User Configuration ---
log_message "Setting up user environment..."

# Create useful aliases
echo "alias ll='ls -AlFht --color=auto --group-directories-first '" >> /home/$USERNAME/.bashrc
echo "alias gs='git status '" >> /home/$USERNAME/.bashrc

# --- Cleanup ---
log_message "Cleaning up..."
apt-get autoremove -y | tee -a $LOG_FILE
apt-get clean -y | tee -a $LOG_FILE

# --- Final Status ---
log_message "=== Setup Complete ==="
log_message "System information:"
log_message "Hostname: $(hostname)"
log_message "IP Address: $(hostname -I | awk '{print $1}')"
log_message "Docker Version: $(docker --version)"
log_message "Docker Compose Version: $(docker compose version)"
log_message "Git Version: $(git --version)"
log_message "Firewall Status:"
ufw status verbose | tee -a $LOG_FILE

log_message "Server setup completed successfully. A log has been saved to $LOG_FILE"
log_message "Please restart your session or run 'newgrp docker' to apply Docker group changes"

# exit 0


