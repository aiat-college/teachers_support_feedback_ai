import requests
import time

print("Sending...")

start = time.time()

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.1:8b",
        "prompt": "Hello",
        "stream": False
    },
    timeout=300
)

print("Returned in", round(time.time() - start, 2), "seconds")
print(response.json())