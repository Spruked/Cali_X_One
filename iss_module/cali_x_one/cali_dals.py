#!/usr/bin/env python3
import asyncio
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent / "scripts"))
from voice_engine import VoiceEngine

async def main():
    ve = VoiceEngine()
    sig_path = Path(__file__).parent / "cali_sig.json"
    if sig_path.exists():
        await ve.speak("Cali online. DALS detected. Awaiting command.")
    else:
        await ve.speak("Cali online. No DALS signature found.")

if __name__ == "__main__":
    asyncio.run(main())