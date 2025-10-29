from sendAudio import solus
import subprocess
from datetime import datetime

now = datetime.now().strftime("%H:%M:%S")

subprocess.Popen(["ollama", "serve"], shell=True)
with open("rag/bootleg_RAG.txt", "r") as context_file:
    lines = context_file.readlines()[-20:]
    context = " ".join([line.strip() for line in lines])

with open("rag/temp_RAG.txt", "a") as mem_context:
    mem_context.write(context)

solus(f"greet the user according to the given time {now}")
context = ""