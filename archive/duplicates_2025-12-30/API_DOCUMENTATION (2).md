# API Documentation

## Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Main Service API (Port 8003)](#main-service-api-port-8003)
- [SKG Service API (Port 8004)](#skg-service-api-port-8004)
- [Python API](#python-api)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Examples](#examples)

## Overview

Cali X One exposes multiple API interfaces for interacting with the Super-Knowledge Graph system:

- **Main Service (Port 8003)**: High-level application interface with web UI
- **SKG Service (Port 8004)**: Direct knowledge graph operations
- **Python API**: Programmatic access via SDK

All APIs support both REST and WebSocket connections for real-time knowledge updates.

## Authentication

### API Key Authentication

```bash
# Set API key in headers
curl -H "X-API-Key: your-api-key" http://localhost:8003/health
```

### JWT Token Authentication

```python
import requests

# Login to obtain JWT
response = requests.post('http://localhost:8003/auth/login', {
    'username': 'your-username',
    'password': 'your-password'
})

token = response.json()['access_token']

# Use token in subsequent requests
headers = {'Authorization': f'Bearer {token}'}
```

## Main Service API (Port 8003)

### Health Check

**GET** `/health`

Check system health and service status.

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2025-01-02T10:30:00Z",
    "services": {
        "skg_core": "operational",
        "curiosity_daemon": "active",
        "contradiction_detector": "monitoring"
    },
    "metrics": {
        "total_triples": 1247,
        "invented_predicates": 5,
        "active_goals": 3
    }
}
```

### Cali X One Signature

**GET** `/sign-cali`

Returns the main Cali X One signature page.

**Response:** HTML page with system information and capabilities demonstration.

### Knowledge Upload

**POST** `/knowledge/upload`

Upload knowledge files in various formats.

**Request Body:**
```json
{
    "format": "triples|json|csv|rdf",
    "data": "file_content_or_base64",
    "source": "optional_source_identifier"
}
```

**Response:**
```json
{
    "success": true,
    "triples_added": 42,
    "bootstrap_triggered": false,
    "new_predicates": []
}
```

### Query Interface

**GET** `/knowledge/query`

Advanced knowledge querying with natural language support.

**Parameters:**
- `q` (string): Natural language query or pattern
- `format` (string): Response format (json|graph|visual)
- `limit` (int): Maximum results (default: 50)

**Example:**
```bash
curl "http://localhost:8003/knowledge/query?q=What connects axioms and proofs?&format=json&limit=10"
```

**Response:**
```json
{
    "query": "What connects axioms and proofs?",
    "results": [
        {
            "subject": "Axiom",
            "predicate": "requires",
            "object": "Proof",
            "confidence": 0.95,
            "level": 0
        }
    ],
    "invented_connections": [
        {
            "predicate": "cluster_foundational_reasoning",
            "entities": ["Axiom", "Proof", "Foundation", "Building"],
            "density": 1.0
        }
    ]
}
```

### Curiosity Goals

**GET** `/curiosity/goals`

Retrieve current autonomous research goals.

**Response:**
```json
{
    "active_goals": [
        "Research identity of UNKNOWN_COMPANY connected to Bob",
        "Investigate relationship between UNKNOWN_RESEARCHER and Alice",
        "Explore patterns in logical-physical domain connections"
    ],
    "completed_goals": 2,
    "daemon_status": "active"
}
```

**POST** `/curiosity/seed`

Seed the curiosity daemon with unknown entities.

**Request Body:**
```json
{
    "unknowns": [
        "UNKNOWN_ENTITY_1",
        "UNKNOWN_PATTERN_X"
    ]
}
```

## SKG Service API (Port 8004)

### Add Knowledge

**POST** `/add`

Add individual knowledge triples to the graph.

**Request Body:**
```json
{
    "s": "subject_entity",
    "p": "predicate_relationship", 
    "o": "object_entity"
}
```

**Response:**
```json
{
    "success": true,
    "triple_id": "uuid-string",
    "level_assigned": 0,
    "bootstrap_check": {
        "total_facts": 51,
        "cascade_triggered": true
    }
}
```

### Batch Add

**POST** `/add_batch`

Add multiple triples in a single operation.

**Request Body:**
```json
{
    "triples": [
        ["Alice", "works_at", "Company_A"],
        ["Bob", "manages", "Team_X"],
        ["Team_X", "develops", "Product_Y"]
    ]
}
```

### Query Knowledge

**GET** `/query`

Query the knowledge graph with pattern matching.

**Parameters:**
- `pat` (array): Pattern [subject, predicate, object] with null for wildcards
- `k` (int): Maximum results to return
- `level` (int): Specific level to query (0, 1, 2, or all)

**Examples:**
```bash
# Find all relationships for Alice
curl "http://localhost:8004/query?pat=[Alice,null,null]&k=10"

# Find all work relationships
curl "http://localhost:8004/query?pat=[null,works_at,null]&k=20"

# Query specific level
curl "http://localhost:8004/query?pat=[null,null,null]&level=1&k=50"
```

**Response:**
```json
{
    "results": [
        {
            "subject": "Alice",
            "predicate": "works_at",
            "object": "Company_A",
            "level": 0,
            "confidence": 1.0
        }
    ],
    "total_matches": 1,
    "query_time_ms": 15
}
```

### Graph Statistics

**GET** `/stats`

Get comprehensive graph statistics.

**Response:**
```json
{
    "levels": {
        "0": {"nodes": 45, "edges": 67},
        "1": {"nodes": 23, "edges": 31}, 
        "2": {"nodes": 12, "edges": 18}
    },
    "invented_predicates": [
        "cluster_foundational_reasoning",
        "cluster_structural_support",
        "cluster_logical_consistency"
    ],
    "bootstrap_status": {
        "triggered": true,
        "threshold_reached": 50,
        "current_facts": 67
    }
}
```

### Expand Graph

**POST** `/expand`

Trigger recursive graph expansion.

**Request Body:**
```json
{
    "force_bootstrap": false,
    "target_level": 2,
    "invention_threshold": 0.3
}
```

### Export Graph

**GET** `/export`

Export the complete knowledge graph.

**Parameters:**
- `format` (string): Export format (json|graphml|pickle|rdf)
- `level` (int): Specific level to export (optional)

**Response:** Graph data in specified format

## Python API

### Core SKG Interface

```python
from skg.core import SKGCore

# Initialize SKG
skg = SKGCore(
    db_path="custom_knowledge.db",
    bootstrap_threshold=50,
    invention_threshold=0.3
)

# Add knowledge
skg.add_triples([
    ('Alice', 'works_at', 'Company'),
    ('Bob', 'manages', 'Alice')
])

# Trigger expansion
skg.expand_recursive()

# Query knowledge
results = skg.query_pattern([None, 'works_at', None])

# Check bootstrap status
if skg.bootstrap_triggered:
    print(f"Bootstrap cascade active with {len(skg.invented_predicates)} new concepts")
```

### High-Level Knowledge Interface

```python
from cali.knowledge import Knowledge

# Simplified interface
kb = Knowledge()

# Natural language queries
results = kb.ask("Who works at Company?")
insights = kb.discover_patterns()

# Autonomous exploration  
kb.enable_curiosity()
goals = kb.get_curiosity_goals()
```

### Event Callbacks

```python
# Register for knowledge events
def on_predicate_invented(predicate, entities, density):
    print(f"New concept invented: {predicate} (density: {density})")

def on_bootstrap_triggered(total_facts):
    print(f"Intelligence cascade activated at {total_facts} facts")

skg.register_callback('predicate_invented', on_predicate_invented)
skg.register_callback('bootstrap_triggered', on_bootstrap_triggered)
```

## Error Handling

### HTTP Status Codes

- `200 OK` - Successful operation
- `201 Created` - Resource created successfully  
- `400 Bad Request` - Invalid request format
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
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

### Common Error Codes

- `INVALID_TRIPLE` - Malformed knowledge triple
- `BOOTSTRAP_ERROR` - Bootstrap cascade failure
- `INVENTION_FAILED` - Predicate invention error
- `QUERY_TIMEOUT` - Query execution timeout
- `GRAPH_CORRUPTED` - Knowledge graph consistency error

## Rate Limiting

### Default Limits

- **Knowledge Addition**: 1000 triples/hour per API key
- **Queries**: 10,000 requests/hour per API key  
- **Graph Export**: 10 exports/hour per API key

### Rate Limit Headers

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 847
X-RateLimit-Reset: 1641062400
```

### Burst Handling

For large knowledge uploads, use the batch endpoints or request rate limit increases for your API key.

## Examples

### Complete AGI Test

```python
import time
from skg.core import SKGCore
from skg.invent_predicate import maybe_invent_predicate

# Initialize system
skg = SKGCore()

# Add cross-domain knowledge
paradoxical_facts = [
    ('Axiom', 'requires', 'Proof'),
    ('Pyramid', 'requires', 'Foundation'),
    ('Logic', 'requires', 'Consistency'),
    ('Building', 'requires', 'Foundation'),
    ('Mathematics', 'builds_on', 'Axiom'),
    ('Architecture', 'builds_on', 'Foundation')
]

# Add facts and cross-domain connections
for fact in paradoxical_facts:
    skg.add_triples([fact])

skg.add_triples([
    ('Axiom', 'analogous_to', 'Foundation'),
    ('Proof', 'similar_to', 'Building'),
    ('Logic', 'parallels', 'Architecture')
])

# Trigger recursive expansion
skg.expand_recursive()

# Enable curiosity daemon
skg.start_curiosity_daemon()

# Force predicate invention
maybe_invent_predicate(skg, thresh=0.3)

# Wait for autonomous processing
time.sleep(5)

# Check results
print(f"Bootstrap triggered: {skg.bootstrap_triggered}")
print(f"Invented predicates: {len(skg.invented_predicates)}")
print(f"Curiosity goals: {len(skg.curiosity_goals)}")

# Demonstrate abstract reasoning
for u, v, d in skg.levels[0].edges(data=True):
    predicate = d.get('predicate', '')
    if 'cluster_' in predicate:
        print(f"Abstract concept discovered: {predicate} connecting {u} ↔ {v}")
```

### WebSocket Real-time Updates

```javascript
// Connect to real-time knowledge updates
const ws = new WebSocket('ws://localhost:8003/ws/knowledge');

ws.onmessage = function(event) {
    const update = JSON.parse(event.data);
    
    switch(update.type) {
        case 'triple_added':
            console.log('New knowledge:', update.data);
            break;
        case 'predicate_invented':
            console.log('New concept invented:', update.data.predicate);
            break;
        case 'bootstrap_triggered':
            console.log('Intelligence cascade activated!');
            break;
        case 'curiosity_goal':
            console.log('New research goal:', update.data.goal);
            break;
    }
};

// Subscribe to specific events
ws.send(JSON.stringify({
    action: 'subscribe',
    events: ['predicate_invented', 'bootstrap_triggered']
}));
```

### Curl Examples

```bash
# Add knowledge via REST
curl -X POST http://localhost:8004/add \
  -H "Content-Type: application/json" \
  -d '{"s": "Python", "p": "is_a", "o": "Programming_Language"}'

# Query with complex pattern
curl "http://localhost:8004/query?pat=[null,requires,null]&k=20" \
  -H "Accept: application/json"

# Get system health
curl http://localhost:8003/health

# Upload knowledge file
curl -X POST http://localhost:8003/knowledge/upload \
  -H "Content-Type: application/json" \
  -d '{
    "format": "triples",
    "data": "Alice,works_at,Company\nBob,manages,Alice\n"
  }'
```

---

**Note**: This API documentation covers the core functionality. For advanced features like distributed deployment, custom predicate invention algorithms, or enterprise authentication, refer to the enterprise documentation or contact support.