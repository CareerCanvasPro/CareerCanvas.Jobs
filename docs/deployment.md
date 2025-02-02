# Deployment Guide

## Prerequisites

- AWS CLI configured with appropriate permissions
- kubectl installed and configured
- Terraform installed
- Docker installed

## Infrastructure Setup

### 1. Initialize Terraform

```bash
cd deployment/terraform
terraform init
terraform plan
terraform apply
```

## Configure Kubernetes

```bash
aws eks update-kubeconfig --region us-east-1 --name careercanvas-cluster
```

3. Deploy Database Migrations

```bash
kubectl apply -f deployment/kubernetes/jobs/db-migration.yaml
```

## Application Deployment

### 1. Build and Push Docker Images

```bash
# Build API Image
docker build -t careercanvas/jobs-api:latest -f deployment/docker/Dockerfile .
docker push careercanvas/jobs-api:latest

# Build Scraper Image
docker build -t careercanvas/jobs-scraper:latest -f deployment/docker/Dockerfile .
docker push careercanvas/jobs-scraper:latest
```

### 2. Deploy Application Components

```bash
# Deploy API
kubectl apply -f deployment/kubernetes/api/
kubectl apply -f deployment/kubernetes/scraper/
```

### 3. Configure DNS and SSL

1. Update Route 53 records to point to ALB
2. Configure ACM certificate
3. Update ALB listener with SSL certificate

## Monitoring Setup

### 1. Deploy Prometheus and Grafana

```bash
kubectl apply -f deployment/kubernetes/monitoring/
```

### 2. Configure CloudWatch

- Set up log groups
- Configure metrics
- Set up alarms

## Backup Configuration

### 1. Database Backups

- Configure automated RDS snapshots
- Set up cross-region replication
- Implement point-in-time recovery

### 2. Application State

- Configure S3 bucket for state backups
- Set up backup rotation policy
- Implement backup verification

## Verification Steps

1. Check API health endpoint
2. Verify metrics collection
3. Test backup restoration
4. Validate SSL configuration
