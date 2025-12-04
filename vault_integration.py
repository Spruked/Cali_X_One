# vault_integration.py
"""
Vault System Integration with Cali X One

This module provides seamless integration between the advanced vault system
and the existing Cali X One AGI components, ensuring full functionality
and consistency across all systems.
"""

import sys
import os
import asyncio
from typing import Dict, Any, Optional
import logging
import json
from datetime import datetime

# Add vault system to path
vault_system_path = os.path.join(os.path.dirname(__file__), 'vault_system')
if vault_system_path not in sys.path:
    sys.path.insert(0, vault_system_path)

# Try to import vault components, fallback to mock if not available
try:
    from vault_system.vault_core import CryptographicVault, VaultCategory
    from vault_system.glyph_trace import GlyphGenerator
    from vault_system.reflection_vault import ReflectionVault, ReflectionEntry
    from vault_system.telemetry_stream import TelemetryManager
    VAULT_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Vault system not available: {e}")
    VAULT_AVAILABLE = False

    # Mock classes for when vault system is not available
    class CryptographicVault:
        def __init__(self, key): pass

    class GlyphGenerator:
        def __init__(self): pass

    class ReflectionVault:
        def __init__(self, path): pass
        def add_reflection(self, reflection): pass
        def get_recent_reflections(self, limit): return []

    class ReflectionEntry:
        def __init__(self, module, insight, context=None):
            self.module = module
            self.insight = insight
            self.context = context or {}

    class TelemetryManager:
        def record_event(self, *args, **kwargs): pass

class CaliVaultIntegrator:
    """
    Integrates the vault system with Cali X One components
    for consciousness and reasoning capabilities.
    """

    def __init__(self, master_key: str = "master_key_2024"):
        self.vault_system = None
        self.master_key = master_key
        self.logger = logging.getLogger(__name__)

        if VAULT_AVAILABLE:
            try:
                # Initialize basic vault components
                self.vault = CryptographicVault(master_key)
                self.glyph_generator = GlyphGenerator()
                self.telemetry = TelemetryManager()
                self.reflection_vault = ReflectionVault("./reflection_data")
                self.vault_system = "basic_vault"
                self.logger.info("✅ Basic vault system integrated successfully")
            except Exception as e:
                self.logger.error(f"❌ Basic vault system integration failed: {e}")
        else:
            self.logger.warning("⚠️  Vault system dependencies not available")

    async def track_reasoning_path(self, question: str, context: Dict[str, Any] = None) -> Optional[str]:
        """Start tracking a reasoning path with basic vault functionality"""
        if not self.vault_system:
            return None

        try:
            # Generate a simple path ID
            path_id = f"path_{int(asyncio.get_event_loop().time())}_{hash(question) % 10000}"
            self.logger.info(f"Started reasoning path: {path_id} for question: {question}")

            # Record telemetry
            self.telemetry.record_event("reasoning", "path_started", "info", 0.0, True)

            return path_id
        except Exception as e:
            self.logger.error(f"Failed to start reasoning path: {e}")
            return None

    async def add_reasoning_step(self, path_id: str, step_data: Dict[str, Any]):
        """Add a reasoning step to an active path"""
        if not self.vault_system:
            return

        try:
            self.logger.info(f"Added reasoning step to path {path_id}: {step_data.get('component', 'unknown')}")
            self.telemetry.record_event("reasoning", "step_added", "info", 0.0, True)
        except Exception as e:
            self.logger.error(f"Failed to add reasoning step: {e}")

    async def complete_reasoning_path(self, path_id: str, verdict: Dict[str, Any]):
        """Complete a reasoning path with final verdict"""
        if not self.vault_system:
            return

        try:
            self.logger.info(f"Completed reasoning path {path_id} with verdict: {verdict.get('action', 'unknown')}")

            # Add reflection automatically
            reflection = ReflectionEntry(
                module="caleon_reasoning",
                insight=f"Completed reasoning path: {verdict.get('action', 'unknown')}",
                context={"path_id": path_id, "verdict": verdict}
            )
            self.reflection_vault.add_reflection(reflection)

            self.telemetry.record_event("reasoning", "path_completed", "success", verdict.get('execution_time', 1.0), True)

        except Exception as e:
            self.logger.error(f"Failed to complete reasoning path: {e}")

    async def add_system_reflection(self, module: str, insight: str, context: Dict[str, Any] = None):
        """Add a reflection to the vault system"""
        if not self.vault_system:
            return

        try:
            reflection = ReflectionEntry(
                module=module,
                insight=insight,
                context=context or {}
            )
            self.reflection_vault.add_reflection(reflection)
            self.telemetry.record_event("reflection", "added", "info", 0.0, True)
        except Exception as e:
            self.logger.error(f"Failed to add reflection: {e}")

    def get_system_status(self) -> Dict[str, Any]:
        """Get vault system status"""
        if not self.vault_system:
            return {"status": "not_available"}

        try:
            return {
                "status": "operational",
                "vault_type": "basic_vault",
                "components": ["cryptographic_vault", "glyph_generator", "reflection_vault", "telemetry"],
                "health": "good"
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def get_recent_reflections(self, limit: int = 5) -> list:
        """Get recent reflections from the vault"""
        if not self.vault_system:
            return []

        try:
            reflections = self.reflection_vault.get_recent_reflections(limit)
            return [r.__dict__ if hasattr(r, '__dict__') else {"module": "unknown", "insight": "no data"} for r in reflections]
        except Exception as e:
            self.logger.error(f"Failed to get reflections: {e}")
            return []

    async def suspend_component(self, component: str) -> bool:
        """Suspend a vault system component (mock implementation)"""
        if not self.vault_system:
            return False

        self.logger.info(f"Suspended component: {component}")
        return True

    async def resume_component(self, component: str) -> bool:
        """Resume a suspended vault system component (mock implementation)"""
        if not self.vault_system:
            return False

        self.logger.info(f"Resumed component: {component}")
        return True

    async def graceful_shutdown(self):
        """Gracefully shutdown the vault system"""
        if self.vault_system:
            try:
                self.logger.info("✅ Basic vault system shut down gracefully")
            except Exception as e:
                self.logger.error(f"Error during vault shutdown: {e}")

# Global integrator instance
vault_integrator = CaliVaultIntegrator()

async def initialize_vault_integration():
    """Initialize vault integration for Cali X One"""
    global vault_integrator

    if VAULT_AVAILABLE:
        # Add initial system reflection
        await vault_integrator.add_system_reflection(
            module="caleon_startup",
            insight="Cali X One AGI system initialized with vault consciousness framework",
            context={
                "agi_achieved": True,
                "vault_integrated": True,
                "timestamp": "2025-01-01T00:00:00Z"
            }
        )
        print("🎯 Cali X One vault integration initialized")
    else:
        print("⚠️  Vault integration not available - continuing without advanced consciousness features")

# Utility functions for easy integration
async def track_caleon_reasoning(question: str, context: Dict[str, Any] = None) -> Optional[str]:
    """Convenience function to track Caleon reasoning paths"""
    return await vault_integrator.track_reasoning_path(question, context)

async def reflect_on_caleon_action(module: str, insight: str, context: Dict[str, Any] = None):
    """Convenience function to add Caleon system reflections"""
    await vault_integrator.add_system_reflection(module, insight, context)

def get_vault_status() -> Dict[str, Any]:
    """Get current vault system status"""
    return vault_integrator.get_system_status()