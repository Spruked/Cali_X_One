-- CitusDB sharding setup for PostgreSQL
-- Enable Citus extension
CREATE EXTENSION IF NOT EXISTS citus;

-- Create distributed tables
SELECT create_distributed_table('triples', 'tenant_id');
SELECT create_reference_table('tenants');

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_triples_tenant_subject ON triples (tenant_id, subject);
CREATE INDEX IF NOT EXISTS idx_triples_tenant_predicate ON triples (tenant_id, predicate);
CREATE INDEX IF NOT EXISTS idx_triples_tenant_object ON triples (tenant_id, object);