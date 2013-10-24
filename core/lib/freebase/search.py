import json
import urllib
from core.config.settings import FREEBASE

service_url = 'https://www.googleapis.com/freebase/v1/search'

params = {
    'key': FREEBASE['api_key'],
    'query': 'gmail'
}
url = service_url + '?' + urllib.urlencode(params)
res = json.loads(urllib.urlopen(url).read())

for val in res['result']:
    response = ''
    response += val['name'] + ' - '
    note = val.get('notable', '')
    if note:
        response += note.get('name', '')
    print response
