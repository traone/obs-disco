import time
import random
from obswebsocket import obsws as ObsWebSocketClient, requests
from flask import Flask, request

# Flask Setup
app = Flask(__name__)

# OBS Connection Settings
OBS_IP = "192.168.89.43" # Henkka's laptop ip
OBS_PORT = 4455
OBS_PASSWORD = "siikrit"

# OBS WebSocket connection placeholder
obs_client = None

# Function to initialize the OBS WebSocket connection
def connect_obs():
    global obs_client
    try:
        obs_client = ObsWebSocketClient(OBS_IP, OBS_PORT, OBS_PASSWORD)
        obs_client.connect()
        print("Connected to OBS WebSocket.")
    except Exception as e:
        obs_client = None 
        print(f"Error connecting to OBS WebSocket: {e}")
        raise e

# Function to close the OBS WebSocket connection
def disconnect_obs():
    global obs_client
    if obs_client:
        try:
            obs_client.disconnect()
            print("Disconnected from OBS WebSocket.")
        except Exception as e:
            print(f"Error disconnecting from OBS WebSocket: {e}")
        finally:
            obs_client = None  # Clean up obs_client

# OBS Functionality
def clip(winAmount):
    global obs_client
    if not obs_client:
        print("OBS WebSocket connection not established.")
        return

    try:
        print("Starting recording in OBS.")
        obs_client.call(requests.ToggleRecord())
        time.sleep(5)
        switch_scene("BigWin")
        time.sleep(5)
        switch_scene("CloseUp")
        #random_number = random.randint(1000, 100000)
        update_win_amount(winAmount)
        time.sleep(5)
        switch_scene("BRB")
        obs_client.call(requests.ToggleRecord())
        print("Recording stopped in OBS.")
    except Exception as e:
        print(f"Error during recording process: {e}")

# Function to switch OBS scene
def switch_scene(scene_name):
    global obs_client
    if not obs_client:
        print("OBS WebSocket connection not established.")
        return

    try:
        obs_client.call(requests.SetCurrentProgramScene(sceneName=scene_name))
    except Exception as e:
        print(f"Failed to switch scene: {e}")

def update_win_amount(amount):
    global obs_client
    if not obs_client:
        print("OBS WebSocket connection not established.")
        return

    try:
        obs_client.call(requests.SetInputSettings(
            inputName="WinAmount",
            inputSettings={"text": str(amount) + "€"},
            overlay=True
        ))
    except Exception as e:
        print(f"Failed to update win amount: {e}")


# Flask route
@app.route('/rec', methods=['POST'])
def rec():
    data = request.json
    winAmount = data.get("winamount")
    clip(int(winAmount))
    #clip()
    return "ok", 200

# Start Flask app
if __name__ == "__main__":
    try:
        connect_obs()  # Establish OBS connection when the app starts
        print("Flask app is running...")
        app.run(host="0.0.0.0", port=5050)
    except KeyboardInterrupt:
        print("\nShutting down Flask app.")
    except Exception as e:
        print(f"Unhandled error: {e}")
    finally:
        disconnect_obs()  # Only disconnect OBS when the app is interrupted or terminated
