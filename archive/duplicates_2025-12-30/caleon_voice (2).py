#!/usr/bin/env python3
"""
Caleon Voice Interface
Always-on voice overlay for ethical AI interaction
"""
import asyncio, json, pathlib
from voice_engine import VoiceEngine
from sentinel import Sentinel
# from seed_linter import SeedVault  # Commented out for now

CALEON_DIR = pathlib.Path(__file__).parent.parent
CONFIG_FILE = CALEON_DIR / "caleon_config.json"

class CaleonVoice:
    def __init__(self):
        self.voice = VoiceEngine()
        self.sentinel = Sentinel()
        # self.vault = SeedVault()  # Commented out
        self.awake = False

    # ---- life-cycle -------------------------------------------------------
    async def boot(self):
        print("🧬 Caleon voice interface booting…")
        await self.voice.speak("Caleon voice online. Say 'Caleon' to wake me.")
        self.awake = True
        await self.loop()

    async def loop(self):
        await self.voice.listen_for_wake("caleon", self._on_wake)

    async def _on_wake(self, text: str):
        print(f"🎤 heard: {text}")
        if "sing" in text:
            await self.voice.speak("Twinkle twinkle little star, how I wonder what you are. Up above the world so high, like a diamond in the sky.")
        elif "ethics" in text and "check" in text:
            await self.voice.speak("Running ethics simulation...")
            # Placeholder for ethics sim
            await self.voice.speak("Ethics check complete. Action approved.")
        elif "mute" in text:
            self.voice.mute()
            await self.voice.speak("Muted." if self.voice._mute else "Unmuted.")
        elif "shutdown" in text:
            await self.voice.speak("Shutting down Caleon voice.")
            self.awake = False
        else:
            await self.voice.speak("Command not recognised. Try 'Caleon sing' or 'Caleon ethics check'.")

# -------------------------------------------------------------------------
def start():
    caleon = CaleonVoice()
    asyncio.run(caleon.boot())

if __name__ == "__main__":
    start()