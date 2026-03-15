import os

# Model configuration
# Set V2T_MODEL environment variable to change the model
# Examples: "tiny.en", "base.en", "small.en", "medium.en", "large"
# Or provide a full path to a GGML model file
MODEL = os.environ.get("V2T_MODEL", "small.en")

# Language configuration
# Set V2T_LANGUAGE to control transcription language:
#   "auto" (default) - automatic language detection (requires multilingual model)
#   "en", "sv", "de", etc. - force a specific language
# Note: .en models (e.g. small.en) are English-only and ignore this setting
LANGUAGE = os.environ.get("V2T_LANGUAGE", "auto")

# Sound configuration
# Set V2T_SOUND to choose sound type:
#   "bloop" (default) - bloop sound effects from wav files
#   "warm" - warm bloop tones with rich harmonics
#   "simple" - simple sine wave tones (880Hz/440Hz)
#   "click" - short click sounds
SOUND_TYPE = os.environ.get("V2T_SOUND", "bloop")
