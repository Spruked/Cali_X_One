#!/usr/bin/env python3
import asyncio
from scripts.voice_engine import VoiceEngine

async def test_voice():
    ve = VoiceEngine()
    await ve.speak("Hello, I am Caleon. Testing voice synthesis.")
    print("Voice test complete.")

if __name__ == "__main__":
    asyncio.run(test_voice())