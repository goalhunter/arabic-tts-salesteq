import os
import json
import uuid
from datetime import datetime
from config import SPEECH_DIR, METADATA_FILE

# Create directories if they don't exist
def ensure_directories(directories):
    """Create directories if they don't exist."""
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

# Load or create metadata
def load_metadata():
    """Load existing metadata or create new empty metadata."""
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"files": []}

def save_metadata(metadata):
    """Save metadata to file."""
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

# Add a new file to metadata
def add_file_to_metadata(filepath, engine, text, dialect=None, original_text=None):
    """Add a new speech file to metadata."""
    metadata = load_metadata()
    file_data = {
        "filepath": filepath,
        "engine": engine,
        "text": text,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Add dialect if provided
    if dialect:
        file_data["dialect"] = dialect
    
    # Add original text if translation was used
    if original_text:
        file_data["original_text"] = original_text
    
    metadata["files"].append(file_data)
    save_metadata(metadata)

def generate_filename(engine, type_prefix="", file_ext=".wav"):
    """Generate a unique filename for a speech file."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = uuid.uuid4().hex[:8]
    
    if type_prefix:
        return f"{engine}_{type_prefix}_{timestamp}_{unique_id}{file_ext}"
    else:
        return f"{engine}_{timestamp}_{unique_id}{file_ext}"