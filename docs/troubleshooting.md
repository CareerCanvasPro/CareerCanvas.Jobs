# Troubleshooting Guide

## Common Issues and Solutions

### API Service

#### 1. API Service Not Starting

**Symptoms:**

- Service fails to start
- HTTP 503 errors

**Solutions:**

1. Check database connectivity:

```bash
kubectl logs deployment/careercanvas-api
```

#### 2. Verify environment variables:

```bash
kubectl describe pod -l app=careercanvas-api
```

#### Check resource constraints:

```bash
kubectl top pod -l app=careercanvas-api
```

## 2. High API Latency

#### Symptoms:

- Slow response times
- Timeout errors

#### Solutions:

1. Check Redis cache status
2. Monitor database performance
3. Review active connections
4. Scale up resources if needed

## Job Scraper

### Scraper Failing

#### Symptoms:

- No new jobs being added
- High error rates in logs

#### Solutions:

1. Check proxy health:

```bash
kubectl logs deployment/careercanvas-scraper | grep "proxy"
```

2. Verify rate limiting settings
3. Check target site accessibility

### 2. Data Quality Issues

#### Symptoms:

- Missing job details
- Incorrect data formats

#### Solutions:

1. Review scraper logs
2. Check data validation rules
3. Update parsing patterns

## Database

#### 1. Connection Issues

#### Symptoms:

- Connection timeouts
- Too many connections

#### Solutions:

1. Check connection pool settings
2. Verify security group rules
3. Monitor RDS metrics

#### 2. Performance Issues

#### Symptoms:

- Slow queries
- High CPU usage

#### Solutions:

1. Review slow query logs
2. Optimize indexes
3. Check query patterns

## Monitoring and Debugging

#### Logging

```bash
# View API logs
kubectl logs -f deployment/careercanvas-api

# View Scraper logs
kubectl logs -f deployment/careercanvas-scraper

# Search for specific errors
kubectl logs deployment/careercanvas-api | grep ERROR
```

### Metrics

- Access Grafana dashboard
- Check CloudWatch metrics
- Monitor resource utilization

### Health Checks

```bash
# API health
curl https://jobs.careercanvas.pro/api/v1/health

# Database health
kubectl exec -it deployment/careercanvas-api -- python -m scripts.check_db

# Cache health
kubectl exec -it deployment/careercanvas-api -- python -m scripts.check_cache
```

## Support and Escalation

### Level 1: Development Team

- Check logs and metrics
- Basic troubleshooting
- Quick fixes

### Level 2: DevOps Team

- Infrastructure issues
- Performance optimization
- Security concerns

### Level 3: Platform Team

- Architecture changes
- Critical failures
- Data recovery
