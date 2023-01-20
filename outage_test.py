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

# Fetch all outages
def get_all_outages():
  response_outages =  requests.get(f"{API_URL}outages", headers={"x-api-key": API_KEY})
  outages = response_outages.json()
  return outages

# Fetch site info
def get_site_info():
  response_norwich = requests.get(f"{API_URL}site-info/{SITE_ID}", headers={"x-api-key": API_KEY})
  norwich_info = response_norwich.json()
  return norwich_info

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
  result = post_response.status_code
  return result

def main():
  outages = get_all_outages()
  info = get_site_info()
  processed = process_data(outages=outages, site_info=info)
  result = post_outages(outages=processed)
  print(result)

if __name__ == "__main__":
  main()