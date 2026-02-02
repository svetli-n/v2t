import numpy as np
import sounddevice as sd

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


def play_start_sound():
    """Play a soft 'bloop' activation sound - low fundamental with rich harmonics."""
    duration_ms = 120

    # Based on analysis: ~140Hz fundamental with harmonics at 240, 350, 450, 613, 767Hz
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


def play_stop_sound():
    """Play a soft confirmation 'bloop' - similar but simpler harmonics."""
    duration_ms = 120

    # Based on analysis: ~140Hz fundamental with simpler harmonics
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
