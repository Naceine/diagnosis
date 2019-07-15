from flask import jsonify

from api.app import app


@app.route('/', methods=['GET'])
def api_index():
    resp = {
        'status': 200,
        'error': None,
    }
    return jsonify(resp)
