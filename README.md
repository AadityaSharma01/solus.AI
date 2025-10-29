# Solus — Local Voice RAG Assistant

Solus is a local, voice-driven retrieval-augmented generation (RAG) assistant. It captures microphone audio, transcribes speech with Whisper (faster-whisper), queries a local LLM endpoint (Ollama / compatible server), and speaks replies using Piper. A small Node/Express server drives a web-based ASCII "face" animation during TTS playback.

This README documents exact, step-by-step setup on Windows (PowerShell), required files, how to run the project, configuration options, and troubleshooting tips.

---

Table of contents
- Project layout
- Requirements & supported platforms
- Files that must be present (voice models, RAG files)
- Step-by-step Windows setup (PowerShell)
- Running the system
- Configuration & usage notes
- Troubleshooting
- Security & license notes

---

Project layout (source files)
- main.py — launcher: starts Ollama, loads initial context, calls solus(...)
- sendAudio.py — main assistant: STT loop, silence detection, calls LLM and Piper TTS
- server.js — small Express server exposing /api/runface for the face animation
- index.html — web UI for the ASCII face (served by server.js)
- init.py — convenience script that spawns node server.js and python main.py
- face.py — (optional) CLI face animation helper
- rag/bootleg_RAG.txt — persistent RAG/context (appended by TTS)
- rag/temp_RAG.txt — temporary/session context (read/written by the app)
- voicemodels/ — folder for Piper voice model files

---

Prerequisites (what to install)
- Windows 10/11 (64-bit)
- Python 3.10 or 3.11 (64-bit)
- Git
- Node.js 18+ (includes npm)
- Ollama (or an LLM server exposing a compatible /api/generate endpoint at localhost:11434) — optional if you plan to test without Ollama
- For better performance (optional): CUDA-compatible GPU and matching drivers if you intend to use use_cuda=True for Piper/Whisper

Recommended Python packages (will be installed below):
- sounddevice
- numpy
- faster-whisper
- requests
- simpleaudio
- pyloudnorm
- piper
- (and any transitive deps such as torch if your Piper or whisper installation requires it)

---

Create a Python virtual environment and install dependencies (PowerShell)
1. Open PowerShell as your user (not Administrator unless needed).
2. Clone repo and switch to project directory:
   ```
   git clone <repo-url> solus
   cd .\solus
   ```
3. Create and activate a venv:
   ```
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   ```
4. Create a requirements file (recommended) and install. Example requirements (you can save this as `requirements.txt` in the repo root):

   ```
   # Save this content as requirements.txt
   sounddevice
   numpy
   faster-whisper
   requests
   simpleaudio
   pyloudnorm
   piper
   ```

   Install:
   ```
   pip install -r requirements.txt
   ```

Note: faster-whisper/piper may require additional system libraries or torch. If a dependency fails, inspect the error and install the matching wheel/torch for your platform.

---

Node.js setup for face/server
1. Ensure Node is installed: `node -v` (recommended v18+).
2. Initialize npm and mark ESM (server.js uses ES modules):
   ```
   npm init -y
   # Edit package.json and add: "type": "module"
   # Or run: (PowerShell)
   (Get-Content package.json) -replace '"main": "index.js",','"main": "index.js",' | Set-Content package.json
   # then manually add "type": "module" in package.json, or run:
   npm pkg set type=module
   ```
3. Install express:
   ```
   npm i express
   ```

---

Voice model files and folders (required)
- Create folder `voicemodels/` in repo root.
- Place Piper voice files inside (used by sendAudio.py):
  - voicemodels/en_US-lessac-medium.onnx
  - voicemodels/en_US-lessac-medium.onnx.json
Notes:
- These ONNX files are not included in the repo. Obtain them from the Piper voice distribution/source you use.
- If you don't have a GPU, set `use_cuda=False` when loading the voice in sendAudio.py.

RAG files (create if missing)
- rag/bootleg_RAG.txt — create empty file:
  ```
  mkdir rag
  New-Item -Path .\rag\bootleg_RAG.txt -ItemType File -Force
  New-Item -Path .\rag\temp_RAG.txt -ItemType File -Force
  ```

---

Ollama / LLM server
- The script expects a local LLM endpoint at `http://localhost:11434/api/generate`. Install and run Ollama (or another server providing a compatible endpoint). Example Ollama start:
  ```
  ollama serve
  ```
- Ensure an appropriate model (e.g. `mistral`) is available to the server. If using Ollama:
  ```
  ollama pull mistral
  ollama serve
  ```
- Quick test the LLM API with PowerShell (replace payload as needed):
  ```
  $body = @{ model='mistral'; prompt='hello'; stream=$false } | ConvertTo-Json
  Invoke-RestMethod -Uri 'http://localhost:11434/api/generate' -Method Post -Body $body -ContentType 'application/json'
  ```

---

Run the system (recommended order)
1. Start the Node server and the assistant via the provided convenience script (PowerShell):
   ```
   python init.py
   ```
   - init.py will spawn the Node server and then start main.py.
   - Alternatively you can run components manually:
     - Start node server:
       ```
       node server.js
       ```
     - Start Ollama (if not running already):
       ```
       ollama serve
       ```
     - In a separate PowerShell terminal, run:
       ```
       python main.py
       ```
2. main.py reads `rag/bootleg_RAG.txt`, appends to `rag/temp_RAG.txt`, calls `solus()` in sendAudio.py and begins audio capture.
3. Speak into the microphone. The assistant transcribes audio and on silence sends the composed prompt to the LLM and synthesizes the reply with Piper.
4. During playback a POST is made to the Node server `/api/runface` so the web face (open http://localhost:5000) animates.

---

Configuration & important variables
- sendAudio.py:
  - sampleRate, chunkSize — audio capture settings
  - silentTime threshold — number of loudness blocks considered silence before sending to LLM
  - voice load: change `use_cuda=True` to `False` if you have no GPU
  - model selection for LLM in `sendToOllama()` — modify the `"model": "mistral"` string if your LLM server uses a different model name
- server.js:
  - PORT (currently 5000) — change if port conflicts exist
  - index.html contains the face animation and polls `/api/runface`

---

Troubleshooting
- Microphone capture fails:
  - Ensure PortAudio is installed and the correct audio device is selected.
  - Run a minimal sounddevice test:
    ```python
    import sounddevice as sd
    print(sd.query_devices())
    ```
- Piper or faster-whisper import errors:
  - Verify installed package names and platform-specific dependencies (torch, CUDA drivers).
- LLM errors (connection refused / JSON decoding)
  - Confirm Ollama (or other server) is running on 11434 and responding to `/api/generate`.
  - Use curl/Invoke-RestMethod to test connectivity.
- Node server errors:
  - Ensure `package.json` contains `"type": "module"` so server.js ESM imports work.
  - Ensure express installed: `npm ls express`
- Face animation not updating:
  - Ensure index.html served at http://localhost:5000 and the assistant POSTs `/api/runface` (sendAudio.py calls this).

---

Security & privacy notes
- Audio and conversation context are written to files under `rag/` — remove or sanitize if you need to purge history.
- This project runs local servers and subprocesses. Do not expose to public networks without proper protections.
- Model usage and voice model licensing: ensure you have the right to use the models you download.

---

Optional improvements / TODOs
- Replace subprocess-based restart of sendAudio.py with an in-process loop to avoid spawning processes.
- Add a requirements.txt and a package.json in repo for reproducible installs.
- Add unit tests for modules that do not require audio/hardware or external servers.
- Add CLI flags to configure ports, model names, and the silence threshold.

---

Example requirements.txt (save in repo root as requirements.txt)
```text
sounddevice
numpy
faster-whisper
requests
simpleaudio
pyloudnorm
piper
```

---

License
- Add your preferred license file (LICENSE) to the repo.

If more granular help is required (example package.json, a requirements.txt added to the repo, or a small script to validate installation), indicate which file you want created and it will be scaffolded.

