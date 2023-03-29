from flask import Flask, request, jsonify
from main import job
from flask import send_from_directory
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["1000 per day"],
    storage_uri="memory://",
)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path != "" and os.path.exists("static/" + path):
        return send_from_directory("static", path)
    else:
        return send_from_directory("static", "index.html")


@app.route("/api/get_advice", methods=["POST"])
@limiter.limit("1/minute", override_defaults=False)
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
