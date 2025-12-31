from asyncio import Semaphore
import logging

logger = logging.getLogger(__name__)

class Bulkhead:
    def __init__(self, db_pool_size: int = 10, analytics_pool_size: int = 5):
        self.db_semaphore = Semaphore(db_pool_size)  # Limit DB calls
        self.analytics_semaphore = Semaphore(analytics_pool_size)  # Limit ML calls
    
    async def isolated_query(self, query_func, pool: str):
        semaphore = getattr(self, f"{pool}_semaphore")
        async with semaphore:
            try:
                return await query_func()
            except Exception as e:
                logger.error(f"Error in isolated query: {e}")
                raise