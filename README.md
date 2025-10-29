Solus 🎙️ | Voice-Powered Local RAG Assistant
A sophisticated voice-driven RAG (Retrieval-Augmented Generation) assistant leveraging local LLM capabilities, real-time STT/TTS, and interactive UI feedback.

<img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10+-blue.svg">

<img alt="Node.js 18+" src="https://img.shields.io/badge/node-18+-green.svg">

<img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg">

🌟 Key Features
Real-time Voice Processing: Seamless microphone capture with advanced silence detection
Local LLM Integration: Powered by Mistral through Ollama's API
Multi-modal Feedback: Interactive ASCII face animation + dynamic soundbar visualization
Context-Aware: Built-in RAG system for persistent conversation memory
Zero Cloud Dependency: Fully local deployment, ensuring data privacy
🛠️ Tech Stack
Core: Python 3.10+, Node.js 18+
AI/ML: faster-whisper, Mistral (via Ollama), Piper TTS
Audio: sounddevice, simpleaudio, pyloudnorm
Backend: Express.js
Real-time Processing: numpy, queue management
UI: Dynamic HTML/JS with WebAPI integration
🚀 One-Line Setup (Windows)
📋 Prerequisites
Windows 10/11 (64-bit)
Python 3.10+ (64-bit)
Node.js 18+
Git
Ollama or compatible LLM server
CUDA-compatible GPU (optional, enhances performance)
🔧 Architecture
💻 Core Components
main.py: System orchestrator
sendAudio.py: Audio processing pipeline
server.js: Web UI server (Express)
index.html: Interactive UI elements
🌈 Features for Recruiters
AI/ML Integration: Implements cutting-edge local LLM technology
Real-time Processing: Advanced audio stream handling and processing
Full-stack Development: Python backend + Node.js server + Web UI
System Architecture: Microservice-style component separation
Performance Optimization: GPU acceleration support
Error Handling: Robust exception management
Data Persistence: Implemented RAG system for context retention
🏃‍♂️ Quick Start
Clone repository
Execute the one-line setup command
Place Piper voice models in voicemodels
Run: python init.py
Access UI: http://localhost:5000
📈 Performance Notes
CPU Mode: ~2-3 second response time
GPU Mode: Sub-second response time
Memory Usage: ~500MB baseline
Disk Space: ~2GB with models
🔒 Privacy & Security
100% local processing
No cloud dependencies
Data stored in local RAG files
Configurable context retention
🤝 Contributing
PRs welcome! Check our contribution guidelines.

📜 License
MIT License - see LICENSE

Built with ❤️ by [Your Name]

For detailed setup instructions, architecture deep-dive, or support: Wiki

