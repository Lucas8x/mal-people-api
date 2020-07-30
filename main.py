from typing import Dict
import requests
from flask import Flask, jsonify
from flask_cors import CORS
from lxml import html

app = Flask(__name__)
CORS(app)


def get_character_info(url: str) -> Dict[str, list]:
  response = requests.get(f'{url}/pictures')
  src = html.fromstring(response.content)
  return {
    'name': ''.join(src.xpath('//*[@class="h1-title"]/text()')).strip().replace("  ", " "),
    'pictures': list(set(src.xpath('//*[@class="js-picture-gallery"]/@href')))
  }


@app.route('/people/<int:people_id>', methods=['GET'])
def fetch(people_id: int):
  print(f'Fetching people with id {people_id}')
  response = requests.get(f'https://myanimelist.net/people/{people_id}')
  src = html.fromstring(response.content)
  characters_links = list(set(src.xpath('//*/td/a[contains(@href, "character")]/@href')))
  characters = [get_character_info(url) for url in characters_links]
  data = {
    'name': ''.join(src.xpath('//*[@class="h1-title"]/text()')),
    'characters': characters
  }
  print(f'Fetch > {people_id} - {data["name"]} < completed')
  return jsonify(data)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3333)
