import time
from functools import cache
from typing import Any, Dict, Optional

import requests
from lxml import html

BASE_URL = 'https://myanimelist.net/people/'
CDN_URL = 'https://cdn.myanimelist.net'


def get_page_src(url: str) -> Optional[Any]:
  try:
    response = requests.get(url)
    src = html.fromstring(response.content)
    return src
  except Exception as e:
    print(e)
    return None


def get_character_info(url: str) -> Optional[Dict]:
  src = get_page_src(f'{url}/pictures')
  if src is None:
    return None

  name = src.xpath('//*[@class="h1-title"]//text()')
  default = src.xpath('//*[contains(@style, "text-align")]/a/img/@data-src')
  pictures = src.xpath('//*[@class="js-picture-gallery"]/@href')
  #favorites = src.xpath('//td[contains(., "Member Favorites")]')

  return {
    'id': 0,
    'name': ''.join(name).strip().replace('  ', ' '),
    'favorites:': None,
    'default': f'{CDN_URL}{default[0]}' if default else None,
    'pictures': pictures if pictures else None
  }


@cache
def get_people_data(people_id: int) -> Dict:
  print(f'Fetching people with id {people_id}')
  people_src = get_page_src(f'{BASE_URL}{people_id}')
  if people_src is None:
    print(f'Fetch > {people_id} < failed.')
    return None

  pictures_src = get_page_src(f'{BASE_URL}{people_id}/*/pics')

  characters_links = people_src.xpath('//*/div/a[contains(@href, "character")]/@href')
  characters_links = list(set(characters_links))

  name = people_src.xpath('//*[@class="h1-title"]//text()')
  favorites = people_src.xpath('//span[contains(., "Member Favorites")]/../text()')
  default = people_src.xpath(f'//*[contains(@href, "{people_id}")]/img/@data-src')
  pictures = pictures_src.xpath('//*[@class="js-picture-gallery"]/@href')
  characters = [get_character_info(url) for url in characters_links]

  data = {
    'id': people_id,
    'name': ''.join(name),
    'favorites': favorites[0].strip() if favorites else None,
    'default': default[0] if default else None,
    'pictures': pictures if pictures else None,
    'characters': characters if characters else None,
  }
  print(f'Fetch > {people_id} - {data["name"]} < completed.')
  return data


if __name__ == '__main__':
  print('scrap')
