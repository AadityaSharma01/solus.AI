# Solus — voice-driven RAG assistant

Small local voice assistant that captures microphone audio, transcribes with Whisper, queries an LLM (via local Ollama-like API), and speaks replies with Piper.

- Entrypoint: [main.py](main.py)  
- Core logic & audio loop: [`sendAudio.solus`](sendAudio.py) in [sendAudio.py](sendAudio.py)  
- Functions referenced:
  - [`sendAudio.callBack`](sendAudio.py) — the sounddevice input callback that queues audio.
  - [`sendAudio.sendToOllama`](sendAudio.py) — posts the composed prompt to the local model API.
  - [`sendAudio.sendToPiper`](sendAudio.py) — synthesizes and plays speech via Piper.
- Model assets:
  - [en_US-lessac-medium.onnx](en_US-lessac-medium.onnx)
  - [en_US-lessac-medium.onnx.json](en_US-lessac-medium.onnx.json)
- Context/state files:
  - [bootleg_RAG.txt](bootleg_RAG.txt)
  - [temp_RAG.txt](temp_RAG.txt)

Quick overview
- Captures audio with sounddevice and measures loudness with pyloudnorm.
- Uses faster_whisper (WhisperModel) for streaming speech-to-text (STT).
- When silence threshold is detected, the collected transcript (`query`) is sent to a local LLM API and the response is synthesized by Piper.
- Conversation context is appended to `bootleg_RAG.txt` and temporary context to `temp_RAG.txt`.

Requirements
- Python 3.10+ recommended
- System deps for sounddevice (ALSA / PortAudio) and simpleaudio
- The repo expects the ONNX Piper voice files in the repo root:
  - [en_US-lessac-medium.onnx](en_US-lessac-medium.onnx)
  - [en_US-lessac-medium.onnx.json](en_US-lessac-medium.onnx.json)

Python dependencies (example)
```sh
pip install sounddevice numpy faster-whisper requests piper-sdk simpleaudio pyloudnorm
