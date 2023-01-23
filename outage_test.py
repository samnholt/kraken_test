import json
import os
import requests
import datetime
import logging

from dateutil import parser, tz
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
SITE_ID = os.getenv("SITE_ID")

selected_outages = []


def return_json(URL: str):
    """'Ensure that program throws an exception in case of 500 status code"""
    response = requests.get(URL, headers={"x-api-key": API_KEY})

    if response.status_code != 500:
        logging.debug('Server is OK')
        json_obj = response.json()
        return json_obj
    else:
        raise Exception("Oops! Request returned a 500")


def get_all_outages():
    """Fetch all outages"""
    logging.info("Fetching all of outages")
    URL = f"{API_URL}outages"
    outages = return_json(URL=URL)
    return outages


def get_site_info():
    """Fetch site info"""
    logging.info("Fetching site info")
    URL = f"{API_URL}site-info/{SITE_ID}"
    site_info = return_json(URL=URL)
    return site_info


def process_data(outages: list, site_info: dict):
    """Process outages, removing those before the given date and outside the site"""
    logging.info("Processing outages")
    for outage in outages:
        if outage["id"] in [device["id"] for device in site_info["devices"]]:
            if parser.parse(outage["begin"]) >= datetime.datetime(
                2022, 1, 1, tzinfo=tz.tzutc()
            ):
                logging.info(f"Found outage matching conditions: {outage['id']}")
                selected_outages.append(outage)

    for selected_outage in selected_outages:
        id = selected_outage["id"]
        for device in site_info["devices"]:
            if device["id"] == id:
                selected_outage["name"] = device["name"]

    logging.info("All relevant outages processed")
    processed_outages = json.dumps(selected_outages)

    return processed_outages


def post_outages(outages: str):
    """Send list of processed outages to post endpoint"""
    logging.info("Posting outages back to endpoint")
    post_response = requests.post(
        f"{API_URL}site-outages/{SITE_ID}",
        headers={
            "x-api-key": API_KEY,
            "accept": "*/*",
            "Content-Type": "application/json",
        },
        data=outages,
    )
    if post_response.status_code != 500:
        result = post_response.status_code
        return result
    else:
        raise Exception("Oops! Request returned a 500.")


def main():
    logging.basicConfig(level=logging.INFO)
    outages = get_all_outages()
    info = get_site_info()
    processed = process_data(outages=outages, site_info=info)
    result = post_outages(outages=processed)
    if result == 200:
        logging.info("Received 200 from POST endpoint - success")


if __name__ == "__main__":
    main()
