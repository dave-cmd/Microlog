import json
import requests
from flask_babel import gettext
from app import app

def translate(text, source_language, dest_language):
    if 'MS_TRANSLATOR_KEY' not in app.config or \
            not app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    
    
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
    payload = f"source={source_language}&q={text}&target={dest_language}"
    headers = {
    'x-rapidapi-host': "google-translate1.p.rapidapi.com",
    'x-rapidapi-key': "409640cd5bmsh04d2c025714ba4fp1e1eafjsncc3296416d7b",
    'accept-encoding': "application/gzip",
    'content-type': "application/x-www-form-urlencoded"
    }
    
    r = requests.request('POST', url, data=payload, headers=headers)
    if r.status_code != 200:
        return gettext('Error: the translation service failed.')
    #return json.loads(r.content.decode('utf-8-sig'))
    str_response = r.json().get('data').get('translations')[0].get('translatedText')
    return r.json()
    #return r.json()