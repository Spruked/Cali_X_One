"""
Bubble Worker - User Interface and CLI Streaming
Handles browser extension communication and terminal streaming
"""

import asyncio
import aiohttp
import json
import os
import websockets
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging
import subprocess
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BubbleWorker:
    def __init__(self, worker_id: str = "bubble-001", registry_url: str = "http://localhost:8003/api/workers"):
        self.worker_id = worker_id
        self.registry_url = registry_url
        self.capabilities = ["ui_streaming", "cli_relay", "extension_bridge"]
        self.endpoint = f"http://localhost:{os.getenv('BUBBLE_PORT', '9997')}"
        self.session: Optional[aiohttp.ClientSession] = None
        self.websocket_server = None
        self.is_registered = False
        self.active_sessions: Dict[str, websockets.WebSocketServerProtocol] = {}

    async def start(self):
        """Start the Bubble worker"""
        self.session = aiohttp.ClientSession()
        await self.register_with_caleon()
        await self.start_heartbeat()
        await self.start_websocket_server()
        logger.info(f"Bubble worker {self.worker_id} started")

    async def stop(self):
        """Stop the worker gracefully"""
        if self.websocket_server:
            self.websocket_server.close()
            await self.websocket_server.wait_closed()

        if self.session:
            await self.session.close()

        logger.info(f"Bubble worker {self.worker_id} stopped")

    async def register_with_caleon(self):
        """Register with the main Caleon service"""
        try:
            registration_data = {
                "worker_id": self.worker_id,
                "worker_type": "bubble_worker",
                "capabilities": self.capabilities,
                "endpoint": self.endpoint,
                "metadata": {
                    "ui_version": "1.0",
                    "websocket_port": 9997,
                    "supported_extensions": ["chrome", "firefox"]
                }
            }

            async with self.session.post(f"{self.registry_url}/register", json=registration_data) as resp:
                if resp.status == 200:
                    self.is_registered = True
                    logger.info("Successfully registered with Caleon")
                else:
                    logger.error(f"Registration failed: {resp.status}")
        except Exception as e:
            logger.error(f"Registration error: {e}")

    async def start_heartbeat(self):
        """Send periodic heartbeats to Caleon"""
        while True:
            try:
                if self.is_registered:
                    heartbeat_data = {
                        "worker_id": self.worker_id,
                        "status": "alive",
                        "load": len(self.active_sessions) * 0.1,  # Load based on active sessions
                        "last_task": f"serving_{len(self.active_sessions)}_sessions"
                    }

                    async with self.session.post(f"{self.registry_url}/heartbeat", json=heartbeat_data) as resp:
                        if resp.status != 200:
                            logger.warning(f"Heartbeat failed: {resp.status}")
                await asyncio.sleep(10)
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                await asyncio.sleep(5)

    async def start_websocket_server(self):
        """Start WebSocket server for extension communication"""
        try:
            self.websocket_server = await websockets.serve(
                self.handle_websocket,
                "localhost",
                9997
            )
            logger.info("WebSocket server started on port 9997")
        except Exception as e:
            logger.error(f"Failed to start WebSocket server: {e}")

    async def handle_websocket(self, websocket, path):
        """Handle WebSocket connections from browser extension"""
        session_id = f"session_{len(self.active_sessions)}"
        self.active_sessions[session_id] = websocket

        try:
            logger.info(f"New WebSocket connection: {session_id}")

            async for message in websocket:
                try:
                    data = json.loads(message)
                    response = await self.process_extension_message(data, session_id)
                    await websocket.send(json.dumps(response))
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({"error": "Invalid JSON"}))
                except Exception as e:
                    logger.error(f"Message processing error: {e}")
                    await websocket.send(json.dumps({"error": str(e)}))

        except websockets.exceptions.ConnectionClosed:
            logger.info(f"WebSocket connection closed: {session_id}")
        finally:
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]

    async def process_extension_message(self, data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Process messages from browser extension"""
        message_type = data.get("type")

        if message_type == "cli_command":
            return await self.execute_cli_command(data.get("command", ""))
        elif message_type == "system_info":
            return await self.get_system_info()
        elif message_type == "ping":
            return {"type": "pong", "timestamp": datetime.now().isoformat()}
        else:
            return {"error": f"Unknown message type: {message_type}"}

    async def execute_cli_command(self, command: str) -> Dict[str, Any]:
        """Execute CLI command and return result"""
        try:
            # Security: whitelist allowed commands
            allowed_commands = ["ls", "pwd", "echo", "date", "whoami"]
            cmd_parts = command.split()

            if not cmd_parts or cmd_parts[0] not in allowed_commands:
                return {"error": "Command not allowed", "command": command}

            # Execute command
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            return {
                "command": command,
                "stdout": stdout.decode().strip(),
                "stderr": stderr.decode().strip(),
                "returncode": process.returncode,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            return {"error": str(e), "command": command}

    async def get_system_info(self) -> Dict[str, Any]:
        """Get system information for extension"""
        return {
            "worker_id": self.worker_id,
            "active_sessions": len(self.active_sessions),
            "server_time": datetime.now().isoformat(),
            "platform": sys.platform,
            "python_version": sys.version
        }

async def main():
    """Main entry point for Bubble worker"""
    worker = BubbleWorker()

    try:
        await worker.start()

        # Keep running
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        logger.info("Shutting down Bubble worker...")
        await worker.stop()

if __name__ == "__main__":
    asyncio.run(main())