import wave
import math
import time
import queue
import requests
import subprocess
import numpy as np
import simpleaudio as sa
import pyloudnorm as pln
import sounddevice as sd
from faster_whisper import WhisperModel
from piper import PiperVoice, SynthesisConfig


def solus(context):
    global passcontext
    replyCount = 0
    model = WhisperModel("small.en", device="cpu", compute_type="int8")

    sampleRate = 16000
    chunkSize = 512

    audio_queue = queue.Queue()
    query = ""

    syn_config = SynthesisConfig(
        volume=1.0,
        length_scale=1.0,
        noise_scale=2.0,
        noise_w_scale=1.5,
        normalize_audio=False,
    )

    voice = PiperVoice.load(
        "voicemodels/en_US-lessac-medium.onnx",
        "voicemodels/en_US-lessac-medium.onnx.json",
        use_cuda=True,
    )

    # STT WHISPER AI
    meter = pln.Meter(sampleRate, block_size=0.01)
    silentTime = [0]
    duration = [0]

    def callBack(indata, frames, time, status):
        if status:
            print(status)
        loudness = meter.integrated_loudness(indata)
        if loudness == -math.inf:
            silentTime[0] += 1
            print(silentTime[0])

            if silentTime[0] >= 60:
                print("Okay now sending to Llama")
                stream.stop()

                sendToOllama()  # FUNCTION DEF AT LINE NUMBER 95

        else:
            silentTime[0] = 0

        audio_queue.put(indata.copy())  ####### IMPORTANT

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

            frame_rate = speaker_wav.getframerate()
            n_frames = speaker_wav.getnframes()

            duration[0] = n_frames / frame_rate
            try:
                subprocess.run("cls", shell=True)

                with open("rag/bootleg_RAG.txt", "a",errors='ignore') as rag_file:
                    rag_file.write(f"\n{dialouge}")
            except FileExistsError:
                print("the file already exists")

            wav_path = "test.wav"
            wav_object = sa.WaveObject.from_wave_file(wav_path)
            
            requests.post("http://localhost:5000/api/runface", json={"time": time.time(), "value": duration[0], "dialouge": dialouge})
            wav_object.play()

            if duration[0] > 5:
                time.sleep(duration[0] - 5)
            elif duration[0] > 2:
                time.sleep(duration[0] - 2)
            else:
                time.sleep(duration[0] + 1)

            subprocess.Popen(["python", "sendAudio.py"], shell=True)

    # LLM OLLAMA NEURAL CHAT
    def sendToOllama():
        req = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": f"""<INSTRUCTIONS>
                            1. RESPOND in a warm and loving tone
                            1. ONLY answer the TASK section
                            2. IGNORE CONTEXT SECTION COMPLETELY - do not reference it, summarize it, or use it unless TASK explicitly asks for it
                            3. If CONTEXT contradicts TASK, follow TASK
                            </INSTRUCTIONS>


                              <TASK>
                                ${query}
                              </TASK>
                            .
                            . IGNORE EVERYTHING BELOW THIS LINE UNLESS DIRECTLY REFERENCED IN THE QUERY ABOVE
                            .
                             <CONTEXT>
                                ${context}
                             </CONTEXT>""",
                "stream": False,
            },
        )
        result = req.json()
        # print(result["response"])
        with open("rag/temp_RAG.txt", "a", errors='ignore') as local_context:
            local_context.write(query + "\n")
        sendToPiper(result["response"])  ##UNCTION DEF LINE NUMBER 77

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
        stream.stop()
        stream.close()
        subprocess.run(["cls"], shell=True)

        with open("rag/temp_RAG.txt", "w") as temp_context_file_clear:
            temp_context_file_clear.write("")


# LOCAL ENTRY POINT
if __name__ == "__main__":
    with open("rag/temp_RAG.txt", "r", errors='ignore') as temp_context_file:
        lines = temp_context_file.readlines()[-100:]
        context = " ".join([line.strip() for line in lines])

    solus(context)

# ============================================================================#
