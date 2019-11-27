from flask import Flask, jsonify, request, abort
import asyncio
import websockets

app = Flask(__name__)
P2P_PORT_NO = 8765
CENTRAL_PORT_NO = 8000

# dummy song dict
songs = {"test": "127.0.0.1"}

@app.route("/")
def home():
    song = request.args.get('song')
    if song not in songs:
        return abort(404)
    return jsonify({"status": 200, "address": songs[song]})

async def alert_download(ip_addr, song):
    uri = "ws://{}:{}".format(ip_addr, CENTRAL_PORT_NO)
    print("connecting")
    async with websockets.connect(uri) as websocket:
        await websocket.send(song)
        print("> {}".format(song))
        await websocket.recv()
        


@app.route("/send_song", methods=['POST'])
def send_song():
    print("here")
    ip_addr = request.args.get('ip_addr')
    song = request.args.get('song')
    asyncio.get_event_loop().run_until_complete(alert_download(ip_addr, song))
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)
