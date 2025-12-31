from pybreaker import CircuitBreaker
import redis
import logging

logger = logging.getLogger(__name__)

class ResilienceManager:
    def __init__(self):
        self.db_breaker = CircuitBreaker(
            fail_max=5,
            reset_timeout=60,
            listeners=[self.log_circuit_state]
        )
        self.redis_client = redis.Redis(host='192.168.142.90', port=6379, db=0)
    
    def log_circuit_state(self, event):
        logger.info(f"Circuit breaker state changed: {event}")
    
    async def protected_db_call(self, query_func):
        return await self.db_breaker.call_async(query_func)