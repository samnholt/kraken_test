import json
import pytest
from outage_test import process_data, return_json

fake_outages = """[
  {
    "id": "002b28fc-283c-47ec-9af2-ea287336dc1b",
    "begin": "2021-07-26T17:09:31.036Z",
    "end": "2021-08-29T00:37:42.253Z"
  },
  {
    "id": "002b28fc-283c-47ec-9af2-ea287336dc1b",
    "begin": "2022-05-23T12:21:27.377Z",
    "end": "2022-11-13T02:16:38.905Z"
  },
  {
    "id": "002b28fc-283c-47ec-9af2-ea287336dc1b",
    "begin": "2022-12-04T09:59:33.628Z",
    "end": "2022-12-12T22:35:13.815Z"
  },
  {
    "id": "04ccad00-eb8d-4045-8994-b569cb4b64c1",
    "begin": "2022-07-12T16:31:47.254Z",
    "end": "2022-10-13T04:05:10.044Z"
  },
  {
    "id": "086b0d53-b311-4441-aaf3-935646f03d4d",
    "begin": "2022-07-12T16:31:47.254Z",
    "end": "2022-10-13T04:05:10.044Z"
  },
  {
    "id": "27820d4a-1bc4-4fc1-a5f0-bcb3627e94a1",
    "begin": "2021-07-12T16:31:47.254Z",
    "end": "2022-10-13T04:05:10.044Z"
  }
]"""

fake_site_info = """{
  "id": "kingfisher",
  "name": "KingFisher",
  "devices": [
    {
      "id": "002b28fc-283c-47ec-9af2-ea287336dc1b",
      "name": "Battery 1"
    },
    {
      "id": "086b0d53-b311-4441-aaf3-935646f03d4d",
      "name": "Battery 2"
    }
  ]
}"""

fake_processed_outages = """[
  {
    "id": "002b28fc-283c-47ec-9af2-ea287336dc1b",
    "name": "Battery 1",
    "begin": "2022-05-23T12:21:27.377Z",
    "end": "2022-11-13T02:16:38.905Z"
  },
  {
    "id": "002b28fc-283c-47ec-9af2-ea287336dc1b",
    "name": "Battery 1",
    "begin": "2022-12-04T09:59:33.628Z",
    "end": "2022-12-12T22:35:13.815Z"
  },
  {
    "id": "086b0d53-b311-4441-aaf3-935646f03d4d",
    "name": "Battery 2",
    "begin": "2022-07-12T16:31:47.254Z",
    "end": "2022-10-13T04:05:10.044Z"
  }
]"""

def test_process_data():
    outages_dict = json.loads(fake_outages)
    site_info_dict = json.loads(fake_site_info)
    processed = process_data(outages=outages_dict, site_info=site_info_dict)
    processed_dict = json.loads(processed)
    fake_processed_outages_dict = json.loads(fake_processed_outages)

    assert processed_dict == fake_processed_outages_dict

def test_return_json():
  with pytest.raises(Exception) as exc_info:
      URL = "https://mock.codes/500"
      return_json(URL=URL)
      assert exc_info.value.args[0] == "Oops! Request returned a 500"