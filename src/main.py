import os
from typing import Any

from flask import Flask, Response, jsonify
from flask_cors import CORS

from src.scrap import get_people_data
#from src.db import redis_queue

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
CORS(app)


@app.route('/people/<int:people_id>')
def fetch_people(people_id: int) -> Any:
  try:
    result = get_people_data(people_id)
    return jsonify(result)
  except Exception as e:
    return jsonify({
      'error': e,
    })


@app.route('/')
def home() -> Response:
  return jsonify({
    'msg': 'https://mal-va-mosaic.vercel.app/',
  })


def server():
  port = int(os.getenv('PORT', 3333))
  app.run(host='0.0.0.0', port=port, debug=os.getenv('isDebug', True))


if __name__ == '__main__':
  server()
