import os
import numpy as np
import sounddevice as sd
import soundfile as sf

from config import SOUND_TYPE

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets", "sounds")
SAMPLE_RATE = 44100


def _apply_envelope(signal, attack_ms=5, decay_ms=50):
    """Apply attack and exponential decay envelope."""
    samples = len(signal)
    attack_samples = int(SAMPLE_RATE * attack_ms / 1000)
    decay_samples = int(SAMPLE_RATE * decay_ms / 1000)

    envelope = np.ones(samples)

    # Quick attack
    if attack_samples > 0 and attack_samples < samples:
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

    # Exponential decay starting after attack
    if decay_samples > 0:
        decay_start = attack_samples
        decay_end = min(samples, decay_start + decay_samples)
        actual_decay = decay_end - decay_start
        if actual_decay > 0:
            # Steeper exponential decay for that "bloop" sound
            envelope[decay_start:decay_end] = np.exp(-np.linspace(0, 6, actual_decay))
            envelope[decay_end:] = 0

    return signal * envelope


def _generate_harmonic_tone(base_freq, duration_ms, harmonics):
    """Generate a tone with specific harmonic frequencies and amplitudes."""
    samples = int(SAMPLE_RATE * duration_ms / 1000)
    t = np.linspace(0, duration_ms / 1000, samples, False)

    tone = np.zeros(samples)
    for freq, amplitude in harmonics:
        tone += amplitude * np.sin(2 * np.pi * freq * t)

    return tone


def _play_start_generated():
    """Play a soft 'bloop' activation sound - low fundamental with rich harmonics."""
    duration_ms = 120

    harmonics = [
        (140, 1.0),    # Fundamental
        (240, 0.37),   # ~1.7x (between 3rd and 4th)
        (350, 0.14),   # ~2.5x
        (450, 0.11),   # ~3.2x
        (613, 0.12),   # ~4.4x
        (767, 0.09),   # ~5.5x
    ]

    tone = _generate_harmonic_tone(140, duration_ms, harmonics)
    tone = _apply_envelope(tone, attack_ms=8, decay_ms=100)

    # Normalize and set volume
    tone = tone / np.max(np.abs(tone))
    sound = (tone * 0.35).astype(np.float32)

    sd.play(sound, samplerate=SAMPLE_RATE)


def _play_stop_generated():
    """Play a soft confirmation 'bloop' - similar but simpler harmonics."""
    duration_ms = 120

    harmonics = [
        (140, 1.0),    # Fundamental
        (243, 0.16),   # ~1.7x
        (413, 0.12),   # ~3x
    ]

    tone = _generate_harmonic_tone(140, duration_ms, harmonics)
    tone = _apply_envelope(tone, attack_ms=8, decay_ms=90)

    # Normalize and set volume (slightly softer than start)
    tone = tone / np.max(np.abs(tone))
    sound = (tone * 0.30).astype(np.float32)

    sd.play(sound, samplerate=SAMPLE_RATE)


def _play_start_click():
    """Play a short click sound to indicate recording started."""
    duration_ms = 20
    samples = int(SAMPLE_RATE * duration_ms / 1000)
    t = np.linspace(0, duration_ms / 1000, samples, False)

    # Click: short burst with multiple high frequencies
    click = (
        np.sin(2 * np.pi * 1000 * t) * 0.5 +
        np.sin(2 * np.pi * 2500 * t) * 0.3 +
        np.sin(2 * np.pi * 4000 * t) * 0.2
    )

    # Sharp exponential decay
    decay = np.exp(-t * 300)
    click = click * decay

    # Normalize and set volume
    click = click / np.max(np.abs(click))
    sound = (click * 0.4).astype(np.float32)

    sd.play(sound, samplerate=SAMPLE_RATE)


def _play_stop_click():
    """Play a short click sound to indicate recording stopped."""
    duration_ms = 25
    samples = int(SAMPLE_RATE * duration_ms / 1000)
    t = np.linspace(0, duration_ms / 1000, samples, False)

    # Lower-pitched click for "done" feel
    click = (
        np.sin(2 * np.pi * 600 * t) * 0.5 +
        np.sin(2 * np.pi * 1500 * t) * 0.3 +
        np.sin(2 * np.pi * 2400 * t) * 0.2
    )

    # Slightly softer decay than start
    decay = np.exp(-t * 250)
    click = click * decay

    # Normalize and set volume
    click = click / np.max(np.abs(click))
    sound = (click * 0.35).astype(np.float32)

    sd.play(sound, samplerate=SAMPLE_RATE)


def _play_start_file():
    """Play the start sound from wav file."""
    data, samplerate = sf.read(os.path.join(ASSETS_DIR, "start.wav"))
    sd.play(data, samplerate)


def _play_stop_file():
    """Play the stop sound from wav file."""
    data, samplerate = sf.read(os.path.join(ASSETS_DIR, "stop.wav"))
    sd.play(data, samplerate)


def _generate_simple_tone(frequency, duration):
    """Generate a simple sine wave tone."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    tone = np.sin(2 * np.pi * frequency * t)
    # Apply fade in/out to avoid clicks
    fade_samples = int(SAMPLE_RATE * 0.01)
    tone[:fade_samples] *= np.linspace(0, 1, fade_samples)
    tone[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    return (tone * 0.3).astype(np.float32)


def _play_start_simple():
    """Play a short high tone to indicate recording started."""
    tone = _generate_simple_tone(880, 0.1)  # A5 note, 100ms
    sd.play(tone, samplerate=SAMPLE_RATE)


def _play_stop_simple():
    """Play a short low tone to indicate recording stopped."""
    tone = _generate_simple_tone(440, 0.1)  # A4 note, 100ms
    sd.play(tone, samplerate=SAMPLE_RATE)


def play_start_sound():
    """Play the start/activation sound."""
    if SOUND_TYPE == "generated":
        _play_start_generated()
    elif SOUND_TYPE == "simple":
        _play_start_simple()
    elif SOUND_TYPE == "click":
        _play_start_click()
    else:
        _play_start_file()


def play_stop_sound():
    """Play the stop/confirmation sound."""
    if SOUND_TYPE == "generated":
        _play_stop_generated()
    elif SOUND_TYPE == "simple":
        _play_stop_simple()
    elif SOUND_TYPE == "click":
        _play_stop_click()
    else:
        _play_stop_file()
