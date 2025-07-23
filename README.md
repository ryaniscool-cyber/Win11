# Win11 from Google Drive

This tool lets you boot a Windows 11 `.iso` file (hosted on Google Drive) on a cloud server.

## How It Works

1. Paste a public Google Drive share link in the frontend (GitHub Pages).
2. The backend:
   - Extracts the file ID
   - Downloads the ISO
   - Boots it in QEMU
   - Streams the screen with VNC (noVNC-compatible)

## Requirements (for backend)

- Python 3
- Flask: `pip install flask requests`
- QEMU: `sudo apt install qemu-system-x86`
- noVNC (optional): `git clone https://github.com/novnc/noVNC.git`

## Run Backend

```bash
python3 app.py
