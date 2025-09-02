# DocuQuery AI - Operations Runbooks

## Overview

This document provides operational runbooks for common incidents and maintenance tasks in the DocuQuery AI system. These runbooks are designed to help operations teams quickly diagnose and resolve issues while maintaining system stability.

## Incident Response Framework

### Severity Levels
- **P0 (Critical)**: System completely down, data loss, security breach
- **P1 (High)**: Major functionality impaired, significant performance degradation
- **P2 (Medium)**: Minor functionality issues, performance impact
- **P3 (Low)**: Cosmetic issues, minor bugs

### Response Times
- **P0**: Immediate response (within 15 minutes)
- **P1**: Response within 1 hour
- **P2**: Response within 4 hours
- **P3**: Response within 24 hours

### Escalation Path
1. **On-call Engineer**: First responder
2. **Team Lead**: Escalation after 30 minutes
3. **Engineering Manager**: Escalation after 2 hours
4. **CTO/VP Engineering**: Escalation after 4 hours

## Common Incidents

### P0: Database Connection Failure

#### Symptoms
- API endpoints returning 500 errors
- Background workers failing
- Database connection timeouts
- High error rates in logs

#### Immediate Actions
1. **Check Database Status**
   ```bash
   # Check PostgreSQL service
   docker-compose -f infra/compose.yml exec postgres pg_isready -U postgres
   
   # Check connection pool
   curl -s http://localhost:8000/health | jq '.dependencies.database'
   ```

2. **Verify Network Connectivity**
   ```bash
   # Test database connectivity
   docker-compose -f infra/compose.yml exec api ping postgres
   
   # Check port availability
   netstat -an | grep 5432
   ```

3. **Check Resource Usage**
   ```bash
   # Monitor system resources
   docker stats postgres
   
   # Check disk space
   df -h
   ```

#### Resolution Steps
1. **Restart Database Service**
   ```bash
   docker-compose -f infra/compose.yml restart postgres
   ```

2. **Verify Recovery**
   ```bash
   # Wait for service to be ready
   sleep 30
   
   # Test connectivity
   docker-compose -f infra/compose.yml exec postgres pg_isready -U postgres
   ```

3. **Check Application Health**
   ```bash
   curl -s http://localhost:8000/health
   ```

#### Prevention
- Monitor database connection pool usage
- Set up automated health checks
- Implement connection retry logic
- Regular database maintenance

### P1: Vector Store (Qdrant) Performance Issues

#### Symptoms
- Slow search response times
- High latency in query endpoints
- Qdrant service unresponsive
- Search timeouts

#### Immediate Actions
1. **Check Qdrant Status**
   ```bash
   # Check service health
   curl -f http://localhost:6333/health
   
   # Check service logs
   docker-compose -f infra/compose.yml logs qdrant
   ```

2. **Monitor Performance Metrics**
   ```bash
   # Check resource usage
   docker stats qdrant
   
   # Monitor response times
   curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:6333/collections"
   ```

3. **Check Collection Status**
   ```bash
   # List collections
   curl -s http://localhost:6333/collections | jq '.'
   
   # Check collection info
   curl -s http://localhost:6333/collections/{collection_name} | jq '.'
   ```

#### Resolution Steps
1. **Restart Qdrant Service**
   ```bash
   docker-compose -f infra/compose.yml restart qdrant
   ```

2. **Optimize Collections**
   ```bash
   # Recreate collection with optimized parameters
   # TODO: Implement collection optimization script
   ```

3. **Scale Resources**
   ```bash
   # Increase memory limits
   docker-compose -f infra/compose.yml up -d --scale qdrant=2
   ```

#### Prevention
- Monitor collection sizes and performance
- Regular index optimization
- Implement search result caching
- Set up performance alerts

### P1: Rate Limiting Spikes

#### Symptoms
- High rate of 429 (Too Many Requests) responses
- API endpoint throttling
- User complaints about service unavailability
- Increased error rates

#### Immediate Actions
1. **Check Rate Limiting Configuration**
   ```bash
   # Review current rate limits
   grep -r "RATE_LIMIT" .env
   
   # Check Redis rate limit data
   docker-compose -f infra/compose.yml exec redis redis-cli
   ```

2. **Monitor Request Patterns**
   ```bash
   # Check API logs for patterns
   docker-compose -f infra/compose.yml logs api | grep "rate_limit"
   
   # Monitor Redis keys
   docker-compose -f infra/compose.yml exec redis redis-cli keys "*rate_limit*"
   ```

3. **Identify Source of Traffic**
   ```bash
   # Check for potential abuse
   docker-compose -f infra/compose.yml logs api | grep -E "(429|rate_limit)"
   
   # Analyze user patterns
   # TODO: Implement traffic analysis script
   ```

#### Resolution Steps
1. **Adjust Rate Limits (Temporary)**
   ```bash
   # Increase limits temporarily
   export RATE_LIMIT_REQUESTS=200
   export RATE_LIMIT_WINDOW=60
   
   # Restart API service
   docker-compose -f infra/compose.yml restart api
   ```

2. **Implement IP Blocking (if abuse detected)**
   ```bash
   # Block abusive IPs
   # TODO: Implement IP blocking mechanism
   ```

3. **Scale API Services**
   ```bash
   # Scale API instances
   docker-compose -f infra/compose.yml up -d --scale api=3
   ```

#### Prevention
- Monitor rate limiting metrics
- Set up alerts for unusual traffic patterns
- Implement progressive rate limiting
- Regular review of rate limit policies

### P2: Redis Connection Issues

#### Symptoms
- Session management failures
- Background task queue issues
- Cache misses
- Connection pool exhaustion

#### Immediate Actions
1. **Check Redis Status**
   ```bash
   # Test Redis connectivity
   docker-compose -f infra/compose.yml exec redis redis-cli ping
   
   # Check service health
   docker-compose -f infra/compose.yml logs redis
   ```

2. **Monitor Connection Pool**
   ```bash
   # Check connection info
   docker-compose -f infra/compose.yml exec redis redis-cli info clients
   
   # Check memory usage
   docker-compose -f infra/compose.yml exec redis redis-cli info memory
   ```

#### Resolution Steps
1. **Restart Redis Service**
   ```bash
   docker-compose -f infra/compose.yml restart redis
   ```

2. **Clear Connection Pool**
   ```bash
   # Flush all data (use with caution)
   docker-compose -f infra/compose.yml exec redis redis-cli flushall
   ```

3. **Verify Recovery**
   ```bash
   # Test connectivity
   docker-compose -f infra/compose.yml exec redis redis-cli ping
   
   # Check application health
   curl -s http://localhost:8000/health
   ```

### P2: Background Task Failures

#### Symptoms
- Document processing stuck
- Embedding generation failures
- Task queue backlog
- Worker service errors

#### Immediate Actions
1. **Check Worker Status**
   ```bash
   # Check worker logs
   docker-compose -f infra/compose.yml logs worker
   
   # Check Celery status
   docker-compose -f infra/compose.yml exec worker celery -A app.background.worker status
   ```

2. **Monitor Task Queue**
   ```bash
   # Check queue length
   docker-compose -f infra/compose.yml exec worker celery -A app.background.worker inspect active
   
   # Check failed tasks
   docker-compose -f infra/compose.yml exec worker celery -A app.background.worker inspect failed
   ```

#### Resolution Steps
1. **Restart Worker Service**
   ```bash
   docker-compose -f infra/compose.yml restart worker
   ```

2. **Clear Failed Tasks**
   ```bash
   # Purge failed tasks
   docker-compose -f infra/compose.yml exec worker celery -A app.background.worker purge
   ```

3. **Scale Workers**
   ```bash
   # Scale worker instances
   docker-compose -f infra/compose.yml up -d --scale worker=3
   ```

## Maintenance Procedures

### Daily Health Checks
1. **Service Status**
   ```bash
   # Check all services
   docker-compose -f infra/compose.yml ps
   
   # Health check endpoints
   curl -s http://localhost:8000/health
   ```

2. **Resource Usage**
   ```bash
   # Monitor system resources
   docker stats --no-stream
   
   # Check disk space
   df -h
   ```

3. **Error Rate Monitoring**
   ```bash
   # Check error logs
   docker-compose -f infra/compose.yml logs --since=1h | grep -i error
   ```

### Weekly Maintenance
1. **Database Maintenance**
   ```bash
   # Vacuum database
   docker-compose -f infra/compose.yml exec postgres vacuumdb -U postgres docuquery_ai
   
   # Analyze tables
   docker-compose -f infra/compose.yml exec postgres psql -U postgres -d docuquery_ai -c "ANALYZE;"
   ```

2. **Log Rotation**
   ```bash
   # Rotate application logs
   # TODO: Implement log rotation script
   ```

3. **Backup Verification**
   ```bash
   # Verify backup integrity
   # TODO: Implement backup verification
   ```

### Monthly Maintenance
1. **Security Updates**
   ```bash
   # Update base images
   docker-compose -f infra/compose.yml pull
   
   # Rebuild services
   docker-compose -f infra/compose.yml build --no-cache
   ```

2. **Performance Review**
   - Review response time metrics
   - Analyze error patterns
   - Optimize database queries
   - Review rate limiting policies

3. **Capacity Planning**
   - Monitor resource usage trends
   - Plan for scaling requirements
   - Review backup and disaster recovery procedures

## Monitoring and Alerting

### Key Metrics
- **Response Time**: API endpoint latency
- **Error Rate**: Percentage of failed requests
- **Throughput**: Requests per second
- **Resource Usage**: CPU, memory, disk, network
- **Queue Length**: Background task backlog

### Alert Thresholds
- **Critical**: Response time > 5s, Error rate > 10%
- **Warning**: Response time > 2s, Error rate > 5%
- **Info**: Response time > 1s, Error rate > 1%

### Alert Channels
- **P0/P1**: Slack + PagerDuty + Phone
- **P2**: Slack + Email
- **P3**: Email only

## Disaster Recovery

### Backup Procedures
1. **Database Backups**
   ```bash
   # Create database backup
   docker-compose -f infra/compose.yml exec postgres pg_dump -U postgres docuquery_ai > backup_$(date +%Y%m%d_%H%M%S).sql
   ```

2. **Configuration Backups**
   ```bash
   # Backup configuration files
   tar -czf config_backup_$(date +%Y%m%d_%H%M%S).tar.gz .env* infra/ scripts/
   ```

3. **Vector Store Backups**
   ```bash
   # Backup Qdrant collections
   # TODO: Implement Qdrant backup script
   ```

### Recovery Procedures
1. **Database Recovery**
   ```bash
   # Restore from backup
   docker-compose -f infra/compose.yml exec -T postgres psql -U postgres docuquery_ai < backup_file.sql
   ```

2. **Service Recovery**
   ```bash
   # Restart all services
   docker-compose -f infra/compose.yml down
   docker-compose -f infra/compose.yml up -d
   ```

3. **Data Verification**
   ```bash
   # Verify data integrity
   curl -s http://localhost:8000/health
   curl -s http://localhost:8000/info
   ```

## Communication Procedures

### Incident Communication
1. **Immediate**: Notify on-call engineer
2. **15 minutes**: Update team via Slack
3. **1 hour**: Send status update to stakeholders
4. **Resolution**: Send incident summary

### Status Page Updates
- **Investigating**: Issue identified, working on resolution
- **Identified**: Root cause found, implementing fix
- **Monitoring**: Fix deployed, monitoring for resolution
- **Resolved**: Issue resolved, normal operations restored

### Post-Incident Review
- **Timeline**: Document incident timeline
- **Root Cause**: Identify root cause
- **Actions**: Document actions taken
- **Lessons Learned**: Identify improvements
- **Follow-up**: Assign action items and due dates
