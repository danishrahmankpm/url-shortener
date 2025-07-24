from flask import Blueprint, request, jsonify, redirect
from app.services import shorten_url, get_original_url, get_stats

bp = Blueprint("routes", __name__)

@bp.route("/api/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing URL"}), 400
    try:
        mapping = shorten_url(data["url"])
        return jsonify({
            "short_code": mapping.short_code,
            "short_url": f"http://localhost:5000/api/{mapping.short_code}"
        }), 201
    except ValueError:
        return jsonify({"error": "Invalid URL"}), 400

@bp.route("/<short_code>", methods=["GET"])
def redirect_to_url(short_code):
    url = get_original_url(short_code)
    if url:
        return redirect(url)
    return jsonify({"error": "Short code not found"}), 404

@bp.route("/api/stats/<short_code>", methods=["GET"])
def stats(short_code):
    stat = get_stats(short_code)
    if stat:
        return jsonify(stat)
    return jsonify({"error": "Short code not found"}), 404
