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
```
pip install sounddevice numpy faster-whisper requests piper-sdk simpleaudio pyloudnorm
```
Adjust package names for your Piper package if it differs.

Run

Start the local LLM service that listens at http://localhost:11434 (the code posts to that URL).
Run the app:
```
This calls sendAudio.solus with the context loaded from bootleg_RAG.txt.
```
Files in this workspace

main.py — loads context and launches the assistant.
sendAudio.py — main implementation: audio capture, STT, LLM request, TTS.
bootleg_RAG.txt — persistent conversation RAG file (appended by Piper).
temp_RAG.txt — temporary/session context (managed by the script).
en_US-lessac-medium.onnx — Piper voice model (binary).
en_US-lessac-medium.onnx.json — Piper voice metadata.
audio-samples/ — (optional) place sample .wav files here.
Notes & tips

The code uses a silence counter to detect end of utterance. Adjust the threshold inside sendAudio.callBack (the silentTime logic) to suit your microphone and room noise.
The Piper synth call expects the ONNX model files in repo root. Confirm the filenames match those in sendAudio.py.
The script currently restarts itself after speaking by invoking python sendAudio.py. You can replace that behavior with a loop or refactor the TTS playback to avoid spawning a subprocess.
Ensure your local LLM server (the endpoint in sendAudio.sendToOllama) is running and the model parameter matches the models available to your server.
Troubleshooting

If microphone capture fails, verify sounddevice/PortAudio installation and the default input device.
If Piper fails to load the model, check file paths and GPU availability (use_cuda=True in sendAudio.py).
If transcription is poor, try a larger Whisper model or enable GPU support for Whisper.

Contact aadirv28@gmail.com

Open issues in this repository for bugs or improvements.

