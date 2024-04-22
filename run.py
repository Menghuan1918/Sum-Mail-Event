import subprocess

def run():
    command = [
        "/home/menghuan/Code/LLM/qwen/server",
        "-m", "/home/menghuan/Code/LLM/qwen/Starling-LM-7B-beta-IQ4_NL.gguf",
        "-c", "4096",
        "--api-key", "1111",
        "--port", "1919",
        "--host", "0.0.0.0",
        "-ngl", "200"
    ]
    process = subprocess.Popen(command)
    return process
    

def stop(process):
    if process:
        process.kill()
        process.wait()