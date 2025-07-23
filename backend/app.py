# backend/app.py
from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_iso():
    iso = request.files['iso']
    iso_path = f"/tmp/{iso.filename}"
    iso.save(iso_path)

    # Kill any previous VM
    os.system("pkill qemu-system-x86_64")

    subprocess.Popen([
        "qemu-system-x86_64",
        "-m", "4096",
        "-enable-kvm",
        "-cdrom", iso_path,
        "-boot", "d",
        "-vnc", ":1",  # noVNC should connect to this
        "-net", "nic",
        "-net", "user"
    ])
    return "ISO uploaded and booting in VM!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
