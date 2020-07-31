import os
from typing import Dict
import requests
from flask import Flask, jsonify, redirect
from flask_cors import CORS
from lxml import html

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)


def get_character_info(url: str) -> Dict[str, list]:
  response = requests.get(f'{url}/pictures')
  src = html.fromstring(response.content)
  return {
    'name': ''.join(src.xpath('//*[@class="h1-title"]/text()')).strip().replace("  ", " "),
    'pictures': src.xpath('//*[@class="js-picture-gallery"]/@href')
  }


@app.route('/people/<int:people_id>', methods=['GET'])
def fetch(people_id: int):
  print(f'Fetching people with id {people_id}')
  response = requests.get(f'https://myanimelist.net/people/{people_id}')
  src = html.fromstring(response.content)
  response2 = requests.get(f'https://myanimelist.net/people/{people_id}/*/pictures')
  src2 = html.fromstring(response2.content)
  characters_links = list(set(src.xpath('//*/td/a[contains(@href, "character")]/@href')))
  data = {
    'name': ''.join(src.xpath('//*[@class="h1-title"]/text()')),
    'pictures': src2.xpath('//*[@class="js-picture-gallery"]/@href'),
    'characters': [get_character_info(url) for url in characters_links],
  }
  print(f'Fetch > {people_id} - {data["name"]} < completed')
  return jsonify(data)


@app.route('/')
def home():
  return redirect('https://lucas8x.github.io/mal-va-mosaic/')


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 3333))
  app.run(host='0.0.0.0', port=port)
