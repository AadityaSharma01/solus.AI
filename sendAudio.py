import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import queue
import requests
import wave
from piper import PiperVoice, SynthesisConfig
import simpleaudio as sa

model = WhisperModel("small.en", device="cpu")

sampleRate = 16000
chunkSize = 512

audio_queue = queue.Queue()
query = ""

syn_config = SynthesisConfig(
    volume=0.5,
    length_scale=1.0,
    noise_scale=1.2,
    noise_w_scale=2.0,
    normalize_audio=False,
)
voice = PiperVoice.load(
    "en_US-lessac-medium.onnx", "en_US-lessac-medium.onnx.json", use_cuda=True
)


# STT WHISPER AI
def callBack(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())


stream = sd.InputStream(
    samplerate=sampleRate, blocksize=chunkSize, channels=1, callback=callBack
)
stream.start()

print("speak into the mic bitch")
buffer = np.zeros((0,), dtype=np.float32)


# TTS PIPER SPEECH
def sendToPiper(dialouge):
    with wave.open("test.wav", "wb") as speaker_wav:
        voice.synthesize_wav(dialouge, speaker_wav)

        wav_path = "test.wav"
        wav_object = sa.WaveObject.from_wave_file(wav_path)
        play_obj = wav_object.play()

        play_obj.wait_done()


# LLM OLLAMA NEURAL CHAT
def sendToOllama():
    req = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "neural-chat", "prompt": query, "stream": False},
    )
    result = req.json()
    print(result["response"])
    sendToPiper(result["response"])

    try:
        with open("bootleg_RAG.txt", "a") as rag_file:
            rag_file.write(query)
    except FileExistsError:
        print("the file already exists")


try:
    while True:
        while not audio_queue.empty():
            data = audio_queue.get()
            buffer = np.concatenate((buffer, data.flatten()))

        if len(buffer) > sampleRate * 0.1:
            segments, _ = model.transcribe(buffer)
            text = " ".join([seg.text for seg in segments])

            if text.strip():
                print(">>", text)
                query += text + " "
            buffer = np.zeros((0,), dtype="float32")


except KeyboardInterrupt:
    print("okay now sending to ollama")
    print(f"{query}")
    stream.stop()
    stream.close()

    sendToOllama()
