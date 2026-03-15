from datetime import datetime
from pynput import keyboard
import numpy as np
import threading
import time
import sys
import signal
import os
from recorder import AudioRecorder
from transcriber import AudioTranscriber
from injector import TextInjector
from sounds import play_start_sound, play_stop_sound

class VoiceToTextApp:
    def __init__(self):
        self.recorder = AudioRecorder()
        self.transcriber = AudioTranscriber()
        self.injector = TextInjector()
        self.is_recording = False
        self.shutdown_event = threading.Event()

        # Recording mode: "toggle" or "push_to_talk"
        # Set via V2T_MODE environment variable (default: toggle)
        self.mode = os.environ.get("V2T_MODE", "toggle").lower()
        if self.mode not in ("toggle", "push_to_talk", "ptt"):
            print(f"Warning: Unknown V2T_MODE '{self.mode}', using 'toggle'")
            self.mode = "toggle"
        if self.mode == "ptt":
            self.mode = "push_to_talk"

        # Hotkey configuration: Right Command
        self.HOTKEY = {keyboard.Key.cmd_r}
        self.current_keys = set()

    def on_press(self, key):
        if key in self.HOTKEY:
            if self.mode == "toggle":
                if self.is_recording:
                    self.stop_recording_and_transcribe()
                else:
                    self.start_recording()
            else:  # push_to_talk
                if not self.is_recording:
                    self.start_recording()

    def on_release(self, key):
        if key in self.HOTKEY:
            if self.mode == "push_to_talk" and self.is_recording:
                self.stop_recording_and_transcribe()

    def start_recording(self):
        play_start_sound()
        self.is_recording = True
        self.recorder.start()
        print("\r🔴 Recording...          ", end="", flush=True)

    def stop_recording_and_transcribe(self):
        play_stop_sound()
        self.is_recording = False
        audio_data = self.recorder.stop()

        if len(audio_data) == 0:
            print("\r⚠️  No audio recorded.    ", flush=True)
            return

        print("\r⏳ Transcribing...       ", end="", flush=True)
        threading.Thread(target=self._process_audio, args=(audio_data,), daemon=True).start()

    def _process_audio(self, audio_data):
        try:
            text = self.transcriber.transcribe(audio_data)
            ts = datetime.now().strftime("%H:%M:%S")
            if text and text != "[BLANK_AUDIO]":
                print(f"\r[{ts}] {text}", flush=True)
                self.injector.type_text(text)
            else:
                print(f"\r[{ts}] ⚠️  No speech detected.", flush=True)
        except Exception as e:
            print(f"\r❌ Error: {e}", flush=True)

    def run(self):
        print(f"Model: {self.transcriber.get_model_name()} | Audio: {self.recorder.get_input_device_info()} | Mode: {self.mode}")
        if self.mode == "toggle":
            print("Press Right Command to toggle recording. Ctrl+C to quit.")
        else:
            print("Hold Right Command to record. Ctrl+C to quit.")
        print()

        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()

        try:
            while not self.shutdown_event.is_set():
                time.sleep(0.1)
        finally:
            listener.stop()
            if self.is_recording:
                self.recorder.stop()

if __name__ == "__main__":
    app = VoiceToTextApp()

    def signal_handler(signum, frame):
        app.shutdown_event.set()

    signal.signal(signal.SIGINT, signal_handler)

    app.run()
    print("\nBye!")
