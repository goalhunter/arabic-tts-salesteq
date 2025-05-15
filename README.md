#Arabic-TTS

A Streamlit application for comparing Arabic Text-to-Speech engines across different dialects.
Setup Instructions
Prerequisites

Python 3.8+
pip (Python package installer)

Installation
# Clone the repository (or download the files)
git clone https://github.com/goalhunter/arabic-tts-salesteq.git
cd arabic-tts

# Create a virtual environment
python -m venv tts-env

# Activate the virtual environment
# On Windows:
tts-env\Scripts\activate
# On macOS/Linux:
source tts-env/bin/activate

# Install dependencies
pip install -r requirements.txt

Configuration
Create a .env file in the project root directory with your API keys:
# Azure Speech API
AZURE_API_KEY=your_azure_key_here
AZURE_REGION=eastus

# ElevenLabs API
ELEVENLABS_API_KEY=your_elevenlabs_key_here

Running the Application
# Start the Streamlit app
streamlit run app.py

The application will be available at: http://localhost:8501
Stopping the Application
Press Ctrl+C in the terminal to stop the Streamlit server.
Deactivating the Virtual Environment
# When you're done, deactivate the virtual environment
deactivate

