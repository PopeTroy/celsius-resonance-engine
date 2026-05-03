import os
import requests
import json
from molecular_compression import synthesize_molecular_assets, organic_amplification

# --- UESP-PRCE CONFIGURATION ---
TARGET_URL = "https://celsiustechmediagroup.co.za"
BRIDGE_URL = os.getenv("BRIDGE_URL")
BRIDGE_KEY = os.getenv("BRIDGE_KEY") # Handshake: 7600
NVIDIA_KEY = os.getenv("NVIDIA_KEY")

def run_resonance_cycle():
    print(f"--- [UESP APEX ENGINE & AMPLIFIER START: {TARGET_URL}] ---")
    
    if not os.path.exists('cdn_assets'):
        os.makedirs('cdn_assets')

    # Cycle 1-3: Molecular Compression (Technical Healing)
    optimized_payloads = synthesize_molecular_assets(TARGET_URL, NVIDIA_KEY)

    # Cycle 4: Organic Amplification (Traffic Generation)
    # This generates SEO-optimized HTML pages to force organic traffic
    seo_payloads = organic_amplification(NVIDIA_KEY)
    
    # Merge all payloads for deployment
    all_payloads = {**optimized_payloads, **seo_payloads}

    # Cycle 5/6: Dual-Path Deployment
    for file_path, content in all_payloads.items():
        # Server Injection via Bridge
        handshake_7600(file_path, content)
        
        # CDN Edge Save
        save_to_edge_node(file_path, content)

    print("--- [RESONANCE ACHIEVED: SITE HEALED & AMPLIFIED] ---")

def save_to_edge_node(file_path, content):
    local_path = os.path.join('cdn_assets', file_path)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    mode = 'w' if isinstance(content, str) else 'wb'
    with open(local_path, mode) as f:
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
            print(f"[7600 OK] {file_path} integrated.")
        else:
            print(f"[7600 FAIL] {file_path} - Status: {response.status_code}")
    except Exception as e:
        print(f"[CRITICAL] Bridge Offline: {e}")

if __name__ == "__main__":
    run_resonance_cycle()
