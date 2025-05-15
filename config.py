import os

# Directory setup
SPEECH_DIR = "generated_speeches"
AZURE_DIR = os.path.join(SPEECH_DIR, "azure")
ELEVEN_DIR = os.path.join(SPEECH_DIR, "elevenlabs")
FACEBOOK_DIR = os.path.join(SPEECH_DIR, "facebook_mms")

# File for storing metadata
METADATA_FILE = os.path.join(SPEECH_DIR, "metadata.json")

# Example texts for different dialects
DIALECT_EXAMPLES = {
    "Modern Standard Arabic": "مرحباً، هذه السيارة مزودة بمحرك توربو سعة 2.0 لتر ونظام ملاحة متقدم.",
    "Najdi Dialect": "مرحبا، هالسيارة فيها محرك تيربو 2.0 لتر ونظام نافيجيشن متطور.",
    "Hijazi Dialect": "هلا، السيارة دي فيها محرك تيربو 2.0 لتر ونظام نافيجيشن زين.",
    "Gulf Dialect": "هلا، هذي السيارة فيها محرك تيربو 2.0 لتر ونظام نافيجيشن ممتاز."
}

# Default English example
DEFAULT_ENGLISH_EXAMPLE = "The car is equipped with a 3.0-liter twin-turbo engine for powerful performance and fuel economy."