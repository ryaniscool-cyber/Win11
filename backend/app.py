# backend/app.py
from flask import Flask, request
import subprocess
import requests
import re
import os

app = Flask(__name__)

def extract_file_id(drive_link):
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", drive_link)
    if match:
        return match.group(1)
    return None

@app.route('/download', methods=['POST'])
def download_and_boot():
    link = request.form.get("link")
    file_id = extract_file_id(link)

    if not file_id:
        return "Invalid Google Drive link.", 400

    # Direct download link (bypasses virus scan warning for large files)
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    iso_path = "/tmp/win11.iso"

    # Download ISO
    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open(iso_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    # Kill previous QEMU if needed
    os.system("pkill qemu-system-x86_64")

    # Start QEMU VM
    subprocess.Popen([
        "qemu-system-x86_64",
        "-m", "4096",
        "-enable-kvm",
        "-cdrom", iso_path,
        "-boot", "d",
        "-vnc", ":1",  # for noVNC
        "-net", "nic",
        "-net", "user"
    ])

    return "ISO is downloading and VM is booting. Open your VNC viewer or browser."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
