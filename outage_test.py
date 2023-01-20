import json
import os
import requests
import datetime

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_URL = os.getenv('API_URL')
SITE_ID = os.getenv('SITE_ID')

selected_outages = []

def return_json(URL):
    response = requests.get(URL, headers={"x-api-key": API_KEY})

    if response.status_code != 500:
      json_obj = response.json()
      return json_obj
    else:
        # Whoops it wasn't a 200
        raise Exception("Oops! Returned a 500")

# Fetch all outages
def get_all_outages():
  URL = f"{API_URL}outages"
  outages = return_json(URL=URL)
  return outages

# Fetch site info
def get_site_info():
  URL = f"{API_URL}site-info/{SITE_ID}"
  site_info = return_json(URL=URL)
  return site_info

# Process outages, removing those before the given date and outside the site
def process_data(outages, site_info):
  for outage in outages:
      if outage['id'] in [device['id'] for device in site_info['devices']]:
          if datetime.datetime.fromisoformat(outage['begin']) >= datetime.datetime.fromisoformat('2022-01-01T00:00:00.000Z'):
            selected_outages.append(outage)

  for selected_outage in selected_outages:
    id = selected_outage['id']
    for device in site_info['devices']:
      if device['id'] == id:
        selected_outage['name'] = device['name']

  processed_outages = json.dumps(selected_outages)

  return processed_outages

# Send list of processed outages to post endpoint
def post_outages(outages):
  post_response = requests.post(f"{API_URL}site-outages/{SITE_ID}", headers={"x-api-key": API_KEY, "accept": "*/*", "Content-Type": "application/json"}, data=outages)
  if post_response.status_code != 500:
    result = post_response.status_code
    return result
  else:
    raise Exception("Oops! Request returned a 500.")

def main():
  outages = get_all_outages()
  info = get_site_info()
  processed = process_data(outages=outages, site_info=info)
  result = post_outages(outages=processed)
  print(result)

if __name__ == "__main__":
  main()