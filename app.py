from flask import Flask, render_template, request, jsonify
from main import job
from flask import send_from_directory
import os

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path != "" and os.path.exists("static/" + path):
        return send_from_directory("static", path)
    else:
        return send_from_directory("static", "index.html")


@app.route("/api/get_advice", methods=["POST"])
def get_advice():
    summoner_name = request.json["summoner_name"]
    if not summoner_name:
        return jsonify({'error': 'Please provide a summoner name.'})

    try:
        advice = job(summoner_name)
        return jsonify({'advice': advice})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
