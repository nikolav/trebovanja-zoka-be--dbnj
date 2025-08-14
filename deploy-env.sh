#!/bin/bash

# config
WSERVER="./wserver.sh"
VARS_PATH="./deploy-vars.sh"
LOG_FILE="./server_setup.log"
DOCKER_COMPOSE_VERSION="v2.27.0"
USERNAME=$(whoami)


# helpers
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}


log_message "Starting server setup process"


# update sys
log_message "Updating package lists..."
apt-get update -y | tee -a $LOG_FILE
apt-get upgrade -y | tee -a $LOG_FILE


# essentials
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



log_message "Installing Docker..."

# remove old versions
apt-get remove -y docker docker-engine docker.io containerd runc | tee -a $LOG_FILE

# docker repository
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# docker components
apt-get update -y | tee -a $LOG_FILE
apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin | tee -a $LOG_FILE

# docker-compose
log_message "Installing Docker Compose $DOCKER_COMPOSE_VERSION..."
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL "https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose


# start on boot
systemctl enable docker.service | tee -a $LOG_FILE
systemctl enable containerd.service | tee -a $LOG_FILE


# firewall
ufw allow OpenSSH | tee -a $LOG_FILE
ufw allow http | tee -a $LOG_FILE
ufw allow https | tee -a $LOG_FILE
ufw allow 'Nginx Full' | tee -a $LOG_FILE
# ufw allow 5000/tcp | tee -a $LOG_FILE
ufw --force enable | tee -a $LOG_FILE


# auto updates
echo 'Unattended-Upgrade::Automatic-Reboot "true";' > /etc/apt/apt.conf.d/50unattended-upgrades
echo 'Unattended-Upgrade::Mail "admin@nikolav.rs";' >> /etc/apt/apt.conf.d/50unattended-upgrades
echo 'Unattended-Upgrade::Automatic-Reboot-Time "03:33";' >> /etc/apt/apt.conf.d/50unattended-upgrades


# load env
if [ -f "$VARS_PATH" ]; then
    log_message "Loading environment variables from $VARS_PATH"
    source "$VARS_PATH"
fi

# executable server:start script
if [ -e "$WSERVER" ]; then
    log_message "Making $WSERVER executable"
    chmod 755 $WSERVER
fi


# aliases
echo "alias ll='ls -AlFht --color=auto --group-directories-first '" >> /home/$USERNAME/.bashrc
echo "alias gs='git status '" >> /home/$USERNAME/.bashrc


# cleanup
log_message "Cleaning up..."
apt-get autoremove -y | tee -a $LOG_FILE
apt-get clean -y | tee -a $LOG_FILE


# status
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

