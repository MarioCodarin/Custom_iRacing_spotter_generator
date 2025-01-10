import random
import requests
from pathlib import Path
import argparse
from pydub import AudioSegment
import io

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate audio samples for iRacing spotter using ElevenLabs API."
    )
    parser.add_argument(
        "--eleven_labs_api_key",
        type=str,
        required=True,
        help="ElevenLabs API key (required)"
    )
    parser.add_argument(
        "--voice_id",
        type=str,
        required=True,
        help="ID of the voice from ElevenLabs (required)"
    )
    parser.add_argument(
        "--voice_name",
        type=str,
        default="CustomSpotter",
        help="Custom name for this voice (default: CustomSpotter)"
    )
    return parser.parse_args()

def parse_spmsg_file(file_path):
    messages = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith(';') and not line.startswith('spmsg'):
                parts = line.split(',', 2)
                if len(parts) == 3:
                    msg_id, wav_file, text = parts
                    messages.append({
                        'msg_id': msg_id.strip(),
                        'wav_file': wav_file.strip(),
                        'text': text.strip().strip('"')
                    })
    return messages

def generate_speech_elevenlabs(
    eleven_labs_api_key: str,
    text: str,
    voice_id: str,
    output_dir: Path,
    output_filename: str,
) -> str:
    wav_file = output_dir / f"{output_filename}.wav"
    if wav_file.exists():
        print(f"Skipped {wav_file} (already exists)")
        return "skipped"

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    payload = {
        "text": text.strip() + ".",
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.9,
            "similarity_boost": 0.7,
            "style": 0.0,
            "use_speaker_boost": False,
        },
        "seed": random.randrange(1, 9999999),
    }
    headers = {
        "Accept": "audio/mpeg",  # Request MP3
        "Content-Type": "application/json",
        "xi-api-key": eleven_labs_api_key
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        # Convert MP3 to WAV with specific settings
        audio = AudioSegment.from_mp3(io.BytesIO(response.content))
        audio = audio.set_frame_rate(44100).set_channels(1).set_sample_width(2)
        
        # Export as WAV
        audio.export(wav_file, format="wav", parameters=["-acodec", "pcm_s16le"])
        
        print(f"Generated {wav_file}")
        return "generated"
    except requests.exceptions.RequestException as e:
        print(f"Error from ElevenLabs API: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return "error"

def generate_audio_samples(
    eleven_labs_api_key: str, voice_name: str, voice_id: str, messages: list
) -> None:
    output_dir = Path(f"voice/spotter_{voice_name}")
    output_dir.mkdir(parents=True, exist_ok=True)

    total_files = 0
    skipped_files = 0
    generated_files = 0

    for message in messages:
        if message['text'] != "NULL" and message['wav_file'] != "NULL":
            result = generate_speech_elevenlabs(
                eleven_labs_api_key=eleven_labs_api_key,
                text=message['text'],
                voice_id=voice_id,
                output_dir=output_dir,
                output_filename=message['wav_file'].replace('.WAV', ''),
            )
            total_files += 1
            if result == "skipped":
                skipped_files += 1
            elif result == "generated":
                generated_files += 1

    print(f"Total files: {total_files}")
    print(f"Skipped files: {skipped_files}")
    print(f"Generated files: {generated_files}")

def create_spmsg_file(messages: list, voice_name: str):
    output_dir = Path(f"voice/spotter_{voice_name}")
    spmsg_file = output_dir / "spmsg.txt"

    with open(spmsg_file, 'w') as file:
        file.write("spmsg01\n\n")
        for message in messages:
            file.write(f"{message['msg_id']}, {message['wav_file']}, \"{message['text']}\"\n")

    print(f"Created spmsg.txt file at {spmsg_file}")

if __name__ == "__main__":
    args = parse_arguments()
    print("Generating audio samples for iRacing spotter using ElevenLabs API...")
    messages = parse_spmsg_file("spmsg sample 2024_12_09.txt")
    generate_audio_samples(args.eleven_labs_api_key, args.voice_name, args.voice_id, messages)
    create_spmsg_file(messages, args.voice_name)
    print(f"Audio samples and spmsg.txt file generated in voice/spotter_{args.voice_name}")
