# models/caleon.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid
import json
from datetime import datetime

Base = declarative_base()

class ClusterNode(Base):
    __tablename__ = "cluster_nodes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    @classmethod
    async def get_or_create(cls, db: AsyncSession, label: str):
        existing = await db.execute(select(cls).filter_by(label=label))
        obj = existing.scalar_one_or_none()
        if obj:
            return obj
        obj = cls(label=label)
        db.add(obj)
        await db.flush()
        return obj

class ClusterEdge(Base):
    __tablename__ = "cluster_edges"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    node_a = Column(Integer, ForeignKey("cluster_nodes.id"), nullable=False)
    node_b = Column(Integer, ForeignKey("cluster_nodes.id"), nullable=False)
    density = Column(Float, nullable=False)
    confidence = Column(Float, default=0.5)
    user_id = Column(String(255), nullable=False)  # from ingest request
    created_at = Column(DateTime, default=datetime.utcnow)
    
    @classmethod
    async def get_or_create(cls, db: AsyncSession, node_a_id: int, node_b_id: int, density: float, user_id: str = None):
        # Assuming user_id is passed, but in the code it's not, wait, need to adjust
        # In the router, it's not passing user_id, so perhaps add it
        existing = await db.execute(select(cls).filter_by(node_a=node_a_id, node_b=node_b_id))
        obj = existing.scalar_one_or_none()
        if obj:
            # Update density if higher
            if density > obj.density:
                obj.density = density
            return obj
        obj = cls(node_a=node_a_id, node_b=node_b_id, density=density, user_id=user_id or "unknown")
        db.add(obj)
        await db.flush()
        return obj
    
    async def cross_user_count(self, db: AsyncSession) -> int:
        # distinct user_id count on this edge
        res = await db.execute(
            select(func.count(func.distinct(ClusterEdge.user_id)))
            .where(ClusterEdge.node_a == self.node_a, ClusterEdge.node_b == self.node_b)
        )
        return res.scalar()

class Predicate(Base):
    __tablename__ = "predicates"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    signature = Column(Text, nullable=False)  # JSON list
    definition = Column(Text)
    confidence = Column(Float, default=0.8)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    @classmethod
    async def get_or_create(cls, db: AsyncSession, name: str, signature: List[str]):
        sig_str = json.dumps(signature)
        existing = await db.execute(select(cls).filter_by(name=name, signature=sig_str))
        obj = existing.scalar_one_or_none()
        if obj:
            obj.fresh = False
            return obj
        obj = cls(name=name, signature=sig_str, definition=f"{name}({','.join(signature)})")
        db.add(obj)
        await db.flush()
        obj.fresh = True
        return obj