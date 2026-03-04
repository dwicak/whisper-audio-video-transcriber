# Whisper Video Transcriber

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![OpenAI Whisper](https://img.shields.io/badge/OpenAI-Whisper-green)](https://github.com/openai/whisper)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful command-line tool to automatically transcribe video and audio files into text using [OpenAI Whisper](https://github.com/openai/whisper). Designed for professionals who need to convert spoken content — such as training videos, briefings, meetings, and lectures — into searchable, editable text documents and subtitle files.

---

## Overview

**Whisper Video Transcriber** leverages OpenAI's state-of-the-art automatic speech recognition (ASR) model, Whisper, to convert the spoken content of any video or audio file into a structured text document. The tool supports two operating modes:

- **Local Mode** — Run entirely offline on your own machine. No data leaves your computer. Ideal for sensitive or confidential content.
- **API Mode** — Send audio to OpenAI's cloud API for faster processing. Requires an OpenAI API key and an internet connection.

The tool automatically extracts the audio track from a video file, processes it through the Whisper model, and outputs both a plain text transcript (`.txt`) and a subtitle file (`.srt`) with precise timestamps for each spoken segment.

---

## Features

- 🎬 **Supports all major video formats** — MP4, MKV, AVI, MOV, WEBM, and more
- 🔊 **Supports all major audio formats** — MP3, WAV, M4A, FLAC, OGG, and more
- 🌐 **Automatic language detection** — or manually specify a language (e.g., Indonesian, English)
- 📄 **Dual output** — generates both `.txt` transcript and `.srt` subtitle file
- 🤖 **Two modes** — Local (offline, free) or OpenAI API (fast, cloud-based)
- 🧠 **Multiple model sizes** — from `tiny` (fast) to `large` (most accurate)
- 🔒 **Privacy-first** — Local mode keeps all data on your machine
- ⚡ **Simple CLI** — easy to use from the terminal with minimal setup

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- [ffmpeg](https://ffmpeg.org/) installed on your system

Install ffmpeg on macOS:
```bash
brew install ffmpeg
```

Install ffmpeg on Ubuntu/Debian:
```bash
sudo apt install ffmpeg
```

---

### Installation

**1. Clone this repository:**
```bash
git clone https://github.com/your-username/whisper-video-transcriber.git
cd whisper-video-transcriber
```

**2. Install Python dependencies:**

For local mode (offline, free):
```bash
pip install openai-whisper moviepy
```

For API mode (OpenAI cloud):
```bash
pip install openai moviepy
```

---

## 🛠️ Usage

### Basic Transcription (Local Mode)
```bash
python3 video_to_text.py --video your_video.mp4
```

### Specify Language (e.g., Indonesian)
```bash
python3 video_to_text.py --video your_video.mp4 --model base --bahasa id
```

### Use a More Accurate Model
```bash
python3 video_to_text.py --video your_video.mp4 --model medium --bahasa id
```

### Transcribe Audio File Directly
```bash
python3 video_to_text.py --video your_audio.mp3 --model base
```

### Use OpenAI API Mode
```bash
python3 video_to_text.py --video your_video.mp4 --use-api --api-key sk-xxxxx
```

### Save Output to a Specific File
```bash
python3 video_to_text.py --video your_video.mp4 --output ~/Documents/hasil_transkripsi.txt
```

---

## Options

| Argument | Description | Default |
|---|---|---|
| `--video` | Path to the video or audio file **(required)** | — |
| `--model` | Whisper model size: `tiny`, `base`, `small`, `medium`, `large` | `base` |
| `--bahasa` | Language code (e.g., `id` for Indonesian, `en` for English) | Auto-detect |
| `--output` | Custom output path for the `.txt` file | Same folder as input |
| `--use-api` | Use OpenAI API instead of local model | `False` |
| `--api-key` | Your OpenAI API key (required when using `--use-api`) | — |

---

## Choosing the Right Model

| Model | Size | RAM Required | Speed | Accuracy |
|---|---|---|---|---|
| `tiny` | 75 MB | ~1 GB | ⚡⚡⚡ Very fast | Fair |
| `base` | 139 MB | ~1 GB | ⚡⚡ Fast | Good |
| `small` | 461 MB | ~2 GB | ⚡ Moderate | Better |
| `medium` | 1.4 GB | ~5 GB | 🐢 Slow | Very good |
| `large` | 2.9 GB | ~10 GB | 🐢🐢 Slowest | Best |

> **Recommendation:** Start with `base` for quick testing. Use `medium` or `large` for production-quality transcription of important content.

---

## Output Files

After a successful transcription, two files will be generated in the same directory as your input file:

| File | Description |
|---|---|
| `your_video_transkripsi.txt` | Full plain text transcript |
| `your_video_transkripsi.srt` | Subtitle file with timestamps (compatible with VLC, YouTube, etc.) |

**Example `.srt` output:**
```
1
00:00:00,000 --> 00:00:04,200
Selamat datang di pelatihan nilai dasar ASN.

2
00:00:04,200 --> 00:00:09,800
Pada sesi ini kita akan membahas nilai akuntabilitas dalam pelayanan publik.
```

---

## Local vs API Mode

| Feature | Local Mode | API Mode |
|---|---|---|
| Cost | Free | $0.006 / minute |
| Internet | Not required | Required |
| Speed | Depends on CPU/GPU | Very fast |
| Privacy | Data stays on your machine | Audio sent to OpenAI servers |
| File size limit | No limit | Max 25 MB |
| Accuracy | Depends on model size | Equivalent to `large` model |

> **For sensitive or confidential content (e.g., government documents, internal meetings), always use Local Mode.**

---

## Supported Languages

Whisper supports over 90 languages including:

- 🇮🇩 Indonesian (`id`)
- 🇬🇧 English (`en`)
- 🇸🇦 Arabic (`ar`)
- 🇯🇵 Japanese (`ja`)
- 🇫🇷 French (`fr`)
- 🇩🇪 German (`de`)
- And many more...

If `--bahasa` is not specified, Whisper will automatically detect the language from the audio.

---

## Requirements

```
openai-whisper
moviepy
openai  (only for API mode)
ffmpeg  (system dependency)
```

---

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a pull request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) — the ASR model powering this tool
- [MoviePy](https://zulko.github.io/moviepy/) — for video and audio processing
- [ffmpeg](https://ffmpeg.org/) — for audio extraction

---

> Built with love for professionals who need fast, accurate, and private transcription of spoken content.
