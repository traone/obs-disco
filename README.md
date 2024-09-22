# Install

1. Create a virtual env `python -m venv obs-disco`
2. Use the venv `source obs-disco/bin/activate`
3. Install dependencies `pip install -r requirements.txt`
4. Modify `src/obs-disco.py` with your corresponding MIDI device name and OBS Scene name.
5. Start server by running `src/obs-disco.py`.
6. Curl to server with the following payload `curl -X POST http://localhost:5050/trigger-event -H "Content-Type: application/json" -d '{"event": "scene_change", "scene_name": "brb2"}'`
