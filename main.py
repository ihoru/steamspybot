import re

import requests

fake_variable = ''  # it's needed to set special order for imports below
from settings import *
from local_settings import *

if not telegram_bot_key:
    print('Empty API key (telegram_bot_key)')
    exit(1)
if not steam_profile:
    print('Empty steam profile name (steam_profile)')
    exit(2)
if not telegram_chat_id:
    print('Empty chat id (telegram_chat_id)')
    exit(3)

telegram_api_url = 'https://api.telegram.org/bot%s/%s'
url = 'http://steamcommunity.com/id/%s?l=%s' % (steam_profile, language)
response = requests.get(url)
content = response.content.decode()
match = re.search('<div class="recentgame_quicklinks recentgame_recentplaytime">\s*<h2>(?P<phrase>.+)</h2>\s*</div>', content, re.MULTILINE | re.UNICODE)
if not match:
    print('Match not found')
    if DEBUG:
        print(content)
    exit(4)

# i.e.: 16.0 ч. за последние 2 недели
phrase = match.group('phrase')

try:
    previous_phrase = open(previous_phrase_cache_file, 'r').read()
except FileNotFoundError:
    previous_phrase = ''
if previous_phrase != phrase:
    file = open(previous_phrase_cache_file, 'w')
    file.write(phrase)
    file.close()
else:
    print('Same phrase as previous')
    exit(0)

data = dict(
    chat_id=telegram_chat_id,
    text=phrase,
)
url = telegram_api_url % (telegram_bot_key, 'sendMessage')
response = requests.post(url, data)
json_content = response.json()
if not json_content:
    print('Sending message error', json_content)
    exit(5)
print('ok')
