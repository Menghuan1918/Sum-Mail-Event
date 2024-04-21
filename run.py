import subprocess
command = "/home/menghuan/Code/LLM/qwen/server -m qwen1_5-7b-chat-q4_0.gguf -c 4096 --api-key 1111 --port 1919 --host 0.0.0.0 -ngl 200"
subprocess.run(command, shell=True)