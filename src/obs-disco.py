from flask import Flask, request, jsonify
import mido
from obswebsocket import obsws, requests
import time  # To add a delay

app = Flask(__name__)

# MIDI Setup
midi_output = mido.open_output('HYDRASYNTH DR')  # Change the MIDI output name to match your Ableton setup

# OBS Setup
obs_ip = "localhost"  # OBS is likely running locally
obs_port = 4455       # OBS WebSocket port
obs_password = "salasana"  # Set this in OBS WebSocket settings
obsws = obsws(obs_ip, obs_port, obs_password)
obsws.connect()


# Function to trigger a MIDI note and keep it on for a longer duration
def trigger_midi(note=10, velocity=100, duration=2.0, channel=1):  # Duration in seconds (increased time)
    try:
        # Send the MIDI 'note_on' message
        midi_output.send(mido.Message('note_on', note=note, velocity=velocity, channel=channel))
        print(f"MIDI note {note} ON sent to {midi_output.name}")
        
        # Wait for the specified duration to keep the note ON
        time.sleep(duration)        
        # Send the MIDI 'note_off' message
        midi_output.send(mido.Message('note_off', note=note, velocity=velocity, channel=channel))
        print(f"MIDI note {note} OFF sent to {midi_output.name}")
        
    except Exception as e:
        print(f"Error sending MIDI: {e}")


# Function to switch OBS scene
# Function to switch OBS scene
def switch_obs_scene(scene_name):
    try:
        obsws.call(requests.SetCurrentProgramScene(sceneName=scene_name))  # Corrected to pass sceneName as a named parameter
    except Exception as e:
        print(f"Failed to switch scene: {e}")

# Mock WebSocket event handler (via HTTP POST)
@app.route('/trigger-event', methods=['POST'])
def trigger_event():
    data = request.json
    print(f"Received event data: {data}")
    
    # Mock condition based on event content (you can change the event criteria here)
    if data.get("event") == "scene_change":
        scene_name = data.get("scene_name", "brb1")  # Fallback to a brb1 scene
        print(f"scenename {scene_name}")
        trigger_midi(note=60, velocity=100)  # Trigger MIDI event
        switch_obs_scene(scene_name)  # Change OBS scene
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "invalid event"}), 400

# Start the Flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)

