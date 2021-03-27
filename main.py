import os
from typing import Dict, Optional, Any
import requests
from flask import Flask, jsonify, redirect
from flask_cors import CORS
from lxml import html

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)


def get_page_src(url: str) -> Optional[Any]:
  response = requests.get(url)
  src = html.fromstring(response.content)
  return src


def get_character_info(url: str) -> Dict:
  src = get_page_src(f'{url}/pictures')

  name = src.xpath('//*[@class="h1-title"]//text()')
  default = src.xpath('//*[contains(@style, "text-align")]/a/img/@data-src')
  pictures = src.xpath('//*[@class="js-picture-gallery"]/@href')

  return {
    'name': ''.join(name).strip().replace('  ', ' '),
    'default': f'https://cdn.myanimelist.net{default[0]}' if default else None,
    'pictures': pictures if pictures else None
  }


@app.route('/people/<int:people_id>')
def fetch(people_id: int) -> Any:
  print(f'Fetching people with id {people_id}')
  people_src = get_page_src(f'https://myanimelist.net/people/{people_id}')
  pictures_src = get_page_src(f'https://myanimelist.net/people/{people_id}/*/pictures')

  characters_links = people_src.xpath('//*/h3/a[contains(@href, "character")]/@href')
  characters_links = list(set(characters_links))

  name = people_src.xpath('//*[@class="h1-title"]//text()')
  default = people_src.xpath(f'//*[contains(@href, "{people_id}")]/img/@data-src')
  pictures = pictures_src.xpath('//*[@class="js-picture-gallery"]/@href')
  characters = [get_character_info(url) for url in characters_links]

  data = {
    'name': ''.join(name),
    'default': default[0] if default else None,
    'pictures': pictures if pictures else None,
    'characters': characters if characters else None,
  }
  print(f'Fetch > {people_id} - {data["name"]} < completed')
  return jsonify(data)


@app.route('/')
def home() -> None:
  return redirect('https://lucas8x.github.io/mal-va-mosaic/')


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 3333))
  app.run(host='0.0.0.0', port=port)
