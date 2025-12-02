#!/usr/bin/env python3
import asyncio
from scripts.voice_engine import VoiceEngine

async def test_recognition():
    ve = VoiceEngine()
    wake_words = [
        "caleon", "cali", "kelly",  # Direct names and misrecognitions
        "hello caleon", "hello cali", "hi caleon", "hi cali",
        "hey caleon", "hey cali", "wake up caleon", "wake up cali",
        "listen caleon", "listen cali", "caleon listen", "cali listen",
        "okay caleon", "okay cali", "hey kelly", "hello kelly"  # More variations
    ]
    print(f"Listening for wake words: {wake_words[:10]}... (and more)")
    print("Say something with one of these words...")

    async def on_wake(text, detected_word):
        print(f"Heard '{detected_word}' in: '{text}'")
        await ve.speak(f"Yes, I heard you say {detected_word}.")
        # Continue listening for testing

    await ve.listen_for_wake(wake_words, on_wake)
    # Keep running
    await asyncio.sleep(60)  # Listen for 60 seconds
    print("Test complete.")

if __name__ == "__main__":
    asyncio.run(test_recognition())