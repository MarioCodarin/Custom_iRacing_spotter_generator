# iRacing Custom Spotter Voice Generator

## Overview
This Python script generates custom audio samples for an iRacing spotter using the ElevenLabs API. It allows you to create personalized voice messages for your iRacing spotter.

## Prerequisites
- Python 3.8+
- ElevenLabs API Key
- A selected voice from ElevenLabs

## Installation
1. Clone the repository
2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

## Usage
```bash
python3 generate_spotter_elevenlabs.py \
    --eleven_labs_api_key YOUR_API_KEY \
    --voice_id YOUR_VOICE_ID \
    --voice_name CustomSpotter
```

### Required Arguments
- `--eleven_labs_api_key`: Your ElevenLabs API key
- `--voice_id`: The ID of the voice you want to use from ElevenLabs

### Optional Arguments
- `--voice_name`: Custom name for your spotter voice (default: CustomSpotter)

## iRacing Installation Instructions

### Audio File Placement
Place the generated audio files in:
```
C:\Program Files (x86)\iRacing\sound\spcc\
```

### Improving Audio Quality
For higher quality spotter audio:
1. Open `Documents\iRacing\app.ini`
2. Find or add the line: `overrideSpccRate = 1`

## Notes
- Requires a sample `spmsg sample 2024_03_07.txt` file with message definitions
- Generated audio files will be in `voice/spotter_[voice_name]` directory
- A `spmsg.txt` file will be generated in the same directory

## Disclaimer
This script requires an active ElevenLabs API subscription. Ensure you comply with ElevenLabs' terms of service.
