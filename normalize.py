"""Python 3, standard library only. Use a server-side environment variable."""
import json
import os
import urllib.request
import urllib.error

HOST = 'crm-lead-hygiene-api.p.rapidapi.com'
CONTACT = {'name': '  Ana   Maria  ', 'email': 'ana@example.COM ',
           'phone': '020 7946 0018', 'country': 'gb',
           'website': 'Example.com/?utm_source=crm'}

def call(path, body, key=None, opener=urllib.request.urlopen):
    key = key or os.environ.get('RAPIDAPI_KEY')
    if not key:
        raise ValueError('Set RAPIDAPI_KEY to your own subscribed RapidAPI application key.')
    request = urllib.request.Request('https://' + HOST + path,
        data=json.dumps(body).encode('utf-8'), method='POST',
        headers={'Content-Type': 'application/json', 'X-RapidAPI-Key': key,
                 'X-RapidAPI-Host': HOST})
    try:
        with opener(request, timeout=15) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        raise RuntimeError('HTTP ' + str(error.code) + ': ' + error.read().decode('utf-8')) from None

if __name__ == '__main__':
    print(json.dumps(call('/v1/contact/normalize', CONTACT), indent=2, ensure_ascii=False))
