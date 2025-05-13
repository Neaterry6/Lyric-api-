import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

LYRICS_OVH_URL = "https://api.lyrics.ovh/v1/"
VAGALUME_URL = "https://api.vagalume.com.br/search.php?art={artist}&mus={song}"

def parse_query(query):
    try:
        if " by " in query:
            song, artist = query.split(" by ", 1)
            return artist.strip(), song.strip()
        return None, None
    except:
        return None, None

@app.route("/lyrics", methods=["GET"])
def get_lyrics():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Provide song name with 'by' format!"}), 400

    artist, song = parse_query(query)
    if not artist or not song:
        return jsonify({"error": "Invalid query format! Try: lyrics Baby Girl by Joeboy"}), 400

    lyrics_data = {}

    try:
        # ✅ Fetch lyrics from Lyrics.ovh
        ovh_response = requests.get(f"{LYRICS_OVH_URL}{artist}/{song}")
        if ovh_response.status_code == 200:
            lyrics_data["Lyrics.ovh"] = ovh_response.json()

        # ✅ Fetch lyrics from Vagalume API
        vagalume_response = requests.get(VAGALUME_URL.format(artist=artist, song=song))
        if vagalume_response.status_code == 200:
            lyrics_data["Vagalume"] = vagalume_response.json()

        if lyrics_data:
            return jsonify(lyrics_data)

        return jsonify({"error": "Lyrics not found!"})

    except Exception as e:
        print("Error:", str(e))  # ✅ Debugging
        return jsonify({"error": f"Server crashed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True
