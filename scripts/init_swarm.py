import os
import requests
import json
from molecular_compression import synthesize_molecular_assets

# --- UESP-PRCE CONFIGURATION ---
TARGET_URL = "https://celsiustechmediagroup.co.za"
BRIDGE_URL = os.getenv("BRIDGE_URL")
BRIDGE_KEY = os.getenv("BRIDGE_KEY") # 7600
NVIDIA_KEY = os.getenv("NVIDIA_KEY")

def run_resonance_cycle():
    print(f"--- [UESP APEX ENGINE START: {TARGET_URL}] ---")
    
    # Create CDN directory if it doesn't exist
    if not os.path.exists('cdn_assets'):
        os.makedirs('cdn_assets')

    # Cycle 1-3: Molecular Compression via NVIDIA NIM
    # 1200 Image Clones & 300 Text Clones execute
    optimized_payloads = synthesize_molecular_assets(TARGET_URL, NVIDIA_KEY)

    # Cycle 5/6: Dual-Path Deployment (Bridge + CDN)
    for file_path, content in optimized_payloads.items():
        # Path 1: The 7600 Bridge (Self-Healing Server)
        handshake_7600(file_path, content)
        
        # Path 2: Local Save for GitHub Pages CDN
        save_to_edge_node(file_path, content)

    print("--- [RESONANCE ACHIEVED: EDGE SYNCED] ---")

def save_to_edge_node(file_path, content):
    """Prepares assets for the GitHub Pages Global Edge."""
    local_path = os.path.join('cdn_assets', file_path)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, 'w' if isinstance(content, str) else 'wb') as f:
        f.write(content)

def handshake_7600(file_path, content):
    payload = {
        'key': BRIDGE_KEY,
        'action': 'heal',
        'file': file_path,
        'content': content
    }
    try:
        response = requests.post(BRIDGE_URL, data=payload, timeout=30)
        if "Successfully Perfected" in response.text:
            print(f"[7600 OK] {file_path} injected.")
        else:
            print(f"[7600 FAIL] {response.status_code}")
    except Exception as e:
        print(f"[CRITICAL] Bridge Offline: {e}")

if __name__ == "__main__":
    run_resonance_cycle()
