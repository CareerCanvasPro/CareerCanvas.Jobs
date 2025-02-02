#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Starting CareerCanvas.Jobs MVP Setup...${NC}"

# Update system packages
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "Installing required packages..."
sudo apt install -y \
    git \
    docker.io \
    docker-compose \
    nginx \
    certbot \
    python3-certbot-nginx

# Configure Docker
echo "Configuring Docker..."
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

# Setup application
echo "Setting up application..."
cd /home/ubuntu
git clone https://github.com/CareerCanvas/CareerCanvas.Jobs.git
cd CareerCanvas.Jobs

# Setup environment
echo "Configuring environment..."
cp .env.example .env

# Configure Nginx
echo "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/careercanvas-jobs <<EOF
server {
    listen 80;
    server_name jobs.careercanvas.pro;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
sudo ln -sf /etc/nginx/sites-available/careercanvas-jobs /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# Start application
echo "Starting application..."
docker-compose up -d

# Setup SSL
echo "Setting up SSL..."
sudo certbot --nginx -d jobs.careercanvas.pro --non-interactive --agree-tos --email admin@careercanvas.pro

echo -e "${GREEN}Setup completed successfully!${NC}"
echo "You can now access the application at: https://jobs.careercanvas.pro"

# Health check
echo "Performing health check..."
sleep 10
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}Application is running successfully!${NC}"
else
    echo -e "${RED}Application health check failed. Please check logs.${NC}"
fi