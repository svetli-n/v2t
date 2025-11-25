from pynput.keyboard import Controller, Key
import time

class TextInjector:
    def __init__(self):
        self.keyboard = Controller()

    def type_text(self, text):
        """
        Type the given text into the currently focused window.
        """
        if not text:
            return
            
        # Add a small delay to ensure focus is correct if called immediately after hotkey release
        time.sleep(0.1)
        
        # Type the text
        self.keyboard.type(text)
        
        # Optional: Add a space after? Or let user decide. 
        # For now, we just type exactly what was transcribed.
        # But often a trailing space is useful if dictating multiple phrases.
        self.keyboard.type(' ')

if __name__ == "__main__":
    print("Testing injector in 3 seconds... Focus a text field!")
    injector = TextInjector()
    time.sleep(3)
    injector.type_text("Hello from Python!")
