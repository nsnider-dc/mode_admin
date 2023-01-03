import json
import requests
import pprint

from requests.auth import HTTPBasicAuth

# import credentials
f = open('creds.json')
data = json.load(f)
# hard code authentication values
host = 'https://modeanalytics.com'
ws = 'beautiful'
un = data['token']
pw = data['password']
# snowflake data source
data_source = 'dca975c09d87'

url = '%s/api/%s/data_sources/%s/reports' % (host, ws, data_source)

r = requests.get(url, auth=HTTPBasicAuth(un, pw))

result = r.json()

print(result)