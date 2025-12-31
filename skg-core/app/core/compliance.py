import psycopg2
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ComplianceManager:
    def __init__(self, db_connection_string: str):
        self.db = psycopg2.connect(db_connection_string)
    
    async def enforce_retention_policy(self, tenant_id: str):
        """Auto-delete data older than retention period"""
        retention_days = await self.get_retention_policy(tenant_id)
        
        cursor = self.db.cursor()
        cursor.execute("""
            DELETE FROM triples 
            WHERE tenant_id = %s 
            AND created_at < NOW() - INTERVAL '%s DAY'
        """, (tenant_id, retention_days))
        self.db.commit()
        logger.info(f"Enforced retention policy for tenant {tenant_id}")
    
    async def get_retention_policy(self, tenant_id: str) -> int:
        # Placeholder - get from config or DB
        return 365  # 1 year default
    
    async def gdpr_erase(self, tenant_id: str, user_id: str):
        """Right to erasure with audit trail"""
        cursor = self.db.cursor()
        
        # Find all triples containing user data
        cursor.execute("""
            SELECT id FROM triples 
            WHERE tenant_id = %s 
            AND (subject LIKE %s OR object LIKE %s)
        """, (tenant_id, f"%{user_id}%", f"%{user_id}%"))
        
        triple_ids = [row[0] for row in cursor.fetchall()]
        
        if triple_ids:
            # Soft delete with tombstones
            cursor.execute("""
                UPDATE triples SET deleted_at = NOW(), gdpr_erased = true 
                WHERE id = ANY(%s)
            """, (triple_ids,))
            self.db.commit()
            
            # Emit erasure event
            await self.emit_event("gdpr.erasure", {
                "tenant_id": tenant_id,
                "user_id": user_id,
                "triples_erased": len(triple_ids),
                "audit_trail": True
            })
    
    async def emit_event(self, topic: str, event: dict):
        # Placeholder - integrate with event sourcing
        logger.info(f"Emitted event {topic}: {event}")