import boto3
import redis
import psycopg2
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class TieredStorage:
    def __init__(self):
        self.hot = redis.Redis(host='192.168.142.90', port=6379, db=0)
        self.warm = psycopg2.connect("dbname=skg user=skg")  # Placeholder
        self.cold = boto3.client('s3', region_name='us-east-1')
    
    async def get_triple(self, triple_id: str, age_days: int):
        if age_days < 7:
            return await self.hot.get(f"triple:{triple_id}")
        elif age_days < 90:
            # Query warm storage
            cursor = self.warm.cursor()
            cursor.execute("SELECT * FROM triples WHERE id = %s", (triple_id,))
            return cursor.fetchone()
        else:
            # Get from S3
            obj = self.cold.get_object(Bucket='skg-cold-storage', Key=f"archived/{triple_id}.parquet")
            return obj['Body'].read()
    
    async def store_triple(self, triple_id: str, data: dict, age_days: int = 0):
        if age_days < 7:
            self.hot.set(f"triple:{triple_id}", str(data))
        elif age_days < 90:
            # Store in warm
            cursor = self.warm.cursor()
            cursor.execute("INSERT INTO triples (id, data) VALUES (%s, %s)", (triple_id, str(data)))
            self.warm.commit()
        else:
            # Store in cold
            self.cold.put_object(Bucket='skg-cold-storage', Key=f"archived/{triple_id}.parquet", Body=str(data))