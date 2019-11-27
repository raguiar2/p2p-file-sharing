from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# dummy song dict
songs = {"test": "127.0.0.1"}

@app.route("/lookup_song")
def home():
    song = request.args.get('song')
    print("song is", song)
    if song not in songs:
        return abort(404)
    return jsonify({"address": songs[song]})
    
if __name__ == "__main__":
    app.run(debug=True)
