from flask import Flask, jsonify, request, send_file
import os

app = Flask(__name__)
PORT_NO = 8000

# dummy song dict
songs = {"test": "127.0.0.1"}

@app.route("/request_song")
def send_song():
    song = request.args.get('song')
    file_bytes = open('./songs/{}.mp3'.format(song), 'rb').read()
    return send_file(file_bytes,
                     attachment_filename='{}.mp3'.format(song),
                     mimetype='audo/mpeg')

if __name__ == "__main__":
    app.run(debug=True, port=PORT_NO)
