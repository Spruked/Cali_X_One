import asyncio, threading, time
import speech_recognition as sr
import pyttsx3

class VoiceEngine:
    def __init__(self):
        self.rec = sr.Recognizer()
        self.mic = sr.Microphone()
        self.tts = pyttsx3.init()
        self._mute = False
        # Set female voice if available
        voices = self.tts.getProperty('voices')
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                self.tts.setProperty('voice', voice.id)
                break

    # ---- TTS --------------------------------------------------------------
    async def speak(self, text: str):
        if self._mute:
            return
        def _speak():
            self.tts.say(text)
            self.tts.runAndWait()
        # Run in thread to not block
        threading.Thread(target=_speak).start()

    # ---- Wake-word --------------------------------------------------------
    async def listen_for_wake(self, wake_words, callback):
        if isinstance(wake_words, str):
            wake_words = [wake_words]
        def _listen():
            with self.mic as source:
                self.rec.adjust_for_ambient_noise(source)
                while True:
                    if self._mute:
                        time.sleep(0.5)
                        continue
                    try:
                        audio = self.rec.listen(source, timeout=0.5, phrase_time_limit=3)
                        txt = self.rec.recognize_google(audio).lower()
                        for word in wake_words:
                            if word in txt:
                                asyncio.run(callback(txt, word))
                                break
                    except sr.WaitTimeoutError:
                        pass
                    except sr.UnknownValueError:
                        pass
        threading.Thread(target=_listen, daemon=True).start()

    def mute(self):
        self._mute = not self._mute