import os
import requests

def push_to_bridge(file_path, content):
    url = os.getenv("BRIDGE_URL")
    key = os.getenv("BRIDGE_KEY") # Frequency: 7600

    payload = {
        'key': key,
        'action': 'heal',
        'file': file_path,
        'content': content
    }

    try:
        response = requests.post(url, data=payload, timeout=30)
        print(f"Bridge Response: {response.text}")
    except Exception as e:
        print(f"Resonance Failure: {e}")
