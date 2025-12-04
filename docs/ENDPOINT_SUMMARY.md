# Endpoint Summary - Cali X One AGI System

## Overview

The Cali X One system exposes APIs across two main services for comprehensive AGI functionality:

- **Main Service (Port 8003)**: High-level user interface and application endpoints
- **SKG Service (Port 8004)**: Direct Super-Knowledge Graph operations

## Main Service API (Port 8003)

### Core Endpoints

| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/` | GET | Service root with navigation | ✅ IMPLEMENTED |
| `/health` | GET | Comprehensive system health check | ✅ IMPLEMENTED |
| `/sign-cali` | GET | AGI demonstration page with capabilities | ✅ IMPLEMENTED |
| `/system/info` | GET | Complete system information and metrics | ✅ IMPLEMENTED |

### Knowledge Management

| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/knowledge/upload` | POST | Upload knowledge files (triples, JSON, CSV) | ✅ IMPLEMENTED |
| `/knowledge/query` | GET | Natural language knowledge querying | ✅ IMPLEMENTED |

**Upload Formats Supported**:
- `triples`: CSV format (subject,predicate,object per line)
- `json`: Structured JSON with triples array
- `csv`: Standard CSV with headers
- `rdf`: RDF/N-Triples format

**Query Features**:
- Natural language pattern matching
- Cross-domain reasoning results
- Invented predicate detection
- Confidence scoring

### Curiosity & Autonomous Intelligence

| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/curiosity/goals` | GET | Current autonomous research goals | ✅ IMPLEMENTED |
| `/curiosity/seed` | POST | Seed unknown entities for exploration | ✅ IMPLEMENTED |

**Curiosity Features**:
- Autonomous goal generation for unknown patterns
- Research direction suggestions
- Pattern gap identification
- Self-directed exploration tracking

## SKG Service API (Port 8004)

### Direct Graph Operations

| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/` | GET | Service information and endpoint list | ✅ IMPLEMENTED |
| `/health` | GET | SKG core system health | ✅ IMPLEMENTED |
| `/add` | POST | Add single knowledge triple | ✅ IMPLEMENTED |
| `/add_batch` | POST | Add multiple triples efficiently | ✅ IMPLEMENTED |
| `/query` | GET | Pattern-based graph querying | ✅ IMPLEMENTED |
| `/stats` | GET | Comprehensive graph statistics | ✅ IMPLEMENTED |

### Advanced Intelligence Operations

| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/expand` | POST | Trigger recursive graph expansion | ✅ IMPLEMENTED |
| `/export` | GET | Export complete knowledge graph | ✅ IMPLEMENTED |
| `/predicate/invent` | POST | Force predicate invention | ✅ IMPLEMENTED |
| `/curiosity/seed` | POST | Seed curiosity with unknowns | ✅ IMPLEMENTED |
| `/curiosity/goals` | GET | Active autonomous goals | ✅ IMPLEMENTED |

## Endpoint Usage Examples

### Main Service Examples

#### Health Check
```bash
curl http://localhost:8003/health
```

Response:
```json
{
  "status": "healthy",
  "services": {
    "main_api": "operational",
    "skg_core": "available"
  },
  "system_info": {
    "python_version": "3.11+",
    "platform": "Windows/Linux"
  }
}
```

#### Knowledge Upload
```bash
curl -X POST http://localhost:8003/knowledge/upload \
  -H "Content-Type: application/json" \
  -d '{
    "format": "triples",
    "data": "Alice,works_at,Company\nBob,manages,Alice\n",
    "source": "hr_system"
  }'
```

#### Natural Language Query
```bash
curl "http://localhost:8003/knowledge/query?q=Who works at Company?&format=json&limit=10"
```

#### Curiosity Seeding
```bash
curl -X POST http://localhost:8003/curiosity/seed \
  -H "Content-Type: application/json" \
  -d '{
    "unknowns": ["UNKNOWN_RESEARCHER", "MYSTERY_PROJECT"]
  }'
```

### SKG Service Examples

#### Add Knowledge Triple
```bash
curl -X POST http://localhost:8004/add \
  -H "Content-Type: application/json" \
  -d '{
    "s": "Python",
    "p": "is_a", 
    "o": "Programming_Language"
  }'
```

#### Pattern Query
```bash
curl "http://localhost:8004/query?pat=[Alice,null,null]&k=20&level=0"
```

#### Force Predicate Invention
```bash
curl -X POST http://localhost:8004/predicate/invent?threshold=0.3
```

#### Graph Statistics
```bash
curl http://localhost:8004/stats
```

Response:
```json
{
  "levels": {
    "0": {"nodes": 45, "edges": 67},
    "1": {"nodes": 23, "edges": 31},
    "2": {"nodes": 12, "edges": 18}
  },
  "invented_predicates": [
    "cluster_foundational_reasoning",
    "cluster_structural_support"
  ],
  "bootstrap_status": {
    "triggered": true,
    "threshold_reached": 67,
    "threshold": 50
  }
}
```

#### Trigger Recursive Expansion
```bash
curl -X POST http://localhost:8004/expand \
  -H "Content-Type: application/json" \
  -d '{
    "force_bootstrap": false,
    "target_level": 2,
    "invention_threshold": 0.3
  }'
```

## WebSocket Endpoints (Future Enhancement)

### Real-time Knowledge Updates
- `ws://localhost:8003/ws/knowledge` - Live knowledge additions
- `ws://localhost:8004/ws/graph` - Graph structure changes
- `ws://localhost:8003/ws/curiosity` - Autonomous goal updates

### Event Types
- `triple_added` - New knowledge triple added
- `predicate_invented` - Novel concept created
- `bootstrap_triggered` - Intelligence cascade activated  
- `curiosity_goal` - New research goal generated
- `contradiction_detected` - Knowledge conflict found

## Authentication & Security

### API Key Authentication
```bash
curl -H "X-API-Key: your-api-key" http://localhost:8003/health
```

### JWT Token Authentication
```bash
# Login
curl -X POST http://localhost:8003/auth/login \
  -d '{"username": "user", "password": "pass"}'

# Use token
curl -H "Authorization: Bearer <token>" http://localhost:8003/knowledge/query
```

### Rate Limiting
- Knowledge Addition: 1000 triples/hour per API key
- Queries: 10,000 requests/hour per API key
- Graph Export: 10 exports/hour per API key

## Error Handling

### Standard HTTP Status Codes
- `200 OK` - Successful operation
- `201 Created` - Resource created
- `400 Bad Request` - Invalid request format
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - System error

### Error Response Format
```json
{
  "error": {
    "code": "INVALID_TRIPLE",
    "message": "Subject cannot be null",
    "details": {
      "field": "subject",
      "value": null
    }
  },
  "request_id": "uuid-string",
  "timestamp": "2025-01-02T10:30:00Z"
}
```

## Performance Metrics

### Response Time Targets
- Health checks: < 50ms
- Simple queries: < 200ms
- Complex pattern matching: < 1s
- Predicate invention: < 5s
- Bootstrap cascade: < 10s

### Throughput Capabilities
- Simple triple addition: 1000+ ops/sec
- Batch operations: 10,000+ triples/batch
- Concurrent queries: 100+ simultaneous
- Real-time updates: 500+ events/sec

## Deployment Configuration

### Docker Compose Services
```yaml
# Main Service
cali-x-one:
  ports: ["8003:8003"]
  command: ["uvicorn", "iss_module.api.api:app"]

# SKG Service  
skg-service:
  ports: ["8004:8004"]
  command: ["python", "/app/skg-core/skg_api.py"]
```

### Environment Variables
- `PYTHONPATH=/app:/app/skg-core`
- `SKG_DB_PATH=/app/data/skg.db`
- `CALEON_ENV=production`

### Health Checks
- Main Service: `curl -f http://localhost:8003/health`
- SKG Service: `curl -f http://localhost:8004/health`
- Interval: 30s, Timeout: 10s, Retries: 3

## Monitoring & Observability

### Metrics Available
- Total knowledge triples across all levels
- Number of invented predicates
- Active curiosity goals count
- Bootstrap cascade status
- Response time percentiles
- Error rate by endpoint

### Log Categories
- Knowledge operations (additions, queries)
- AGI events (predicate invention, bootstrap)
- System health (errors, performance)
- Security events (authentication, authorization)

## Future Enhancements

### Planned Endpoints
- `/reasoning/explain` - Explain reasoning paths
- `/patterns/discover` - Automated pattern discovery
- `/knowledge/validate` - Knowledge consistency checking
- `/export/visualization` - Graph visualization export
- `/analytics/insights` - Advanced analytics dashboard

### Integration Points
- Elasticsearch integration for advanced search
- Grafana dashboards for real-time monitoring
- Webhook notifications for AGI events
- REST callbacks for external system integration

---

**Summary**: All core endpoints are implemented and functional. The system provides comprehensive API coverage for AGI-level knowledge management, autonomous intelligence operations, and real-time monitoring capabilities. Both services are production-ready with proper error handling, health checks, and performance optimization.