import requests
import zipfile
import io
import os
import sys
import pandas as pd
import shutil
import numpy as np
import argparse

# qualtrics user ID --> used for API calls
QUALTRICS_USER = "YOUR_USER_ID"
# argument parser for directory and survey list
parser = argparse.ArgumentParser(description='Download surveys.')
parser.add_argument('data_dir', type=str, help='Data directory')
parser.add_argument('csv_file', type=str, help='CSV file with survey names and IDs')
args = parser.parse_args()

# file directories
DATA_DIR = args.data_dir

# set api token from os.environ --> only on your environment will this work
try:
    API_TOKEN = os.environ["X_API_TOKEN"]
except KeyError:
    print("set environment variable X_API_TOKEN")
    sys.exit(2)

# read survey names and ids from csv file --> arguments from script call
surveys = pd.read_csv(args.csv_file)
survey_name_list = surveys['SurveyName'].tolist()
survey_id_list = surveys['SurveyID'].tolist()

# the below function downloads all of the qualtrics surveys in a given list and saves them to a given directory
def download_qualtrics(directory, user, api_token, survey_id, survey_name):
    # Setting static parameters
    file_format = "csv"
    data_center = "your.qualtrics.datacenter"
    request_progress = 0.0
    progress_check = "In progress."
    base_url = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/".format(data_center, survey_id)
    headers = {
            "content-type": "application/json",
            "x-api-token": api_token,
            }

    # Creating Data Export
    download_request_format = '{"format":"' + file_format + '", "useLabels":"True"}'
    download_request = requests.request("POST", base_url, data=download_request_format, headers=headers)
    progress_check_id = download_request.json()["result"]["progressId"]

    # Checking on Data Export progress_check and waiting until export is ready
    while progress_check != "complete" and progress_check != "failed":
        requestCheckUrl = base_url + progress_check_id
        request_check = requests.request("GET", requestCheckUrl, headers=headers)
        request_progress = request_check.json()["result"]["percentComplete"]
        progress_check = request_check.json()["result"]["status"]

    # Check for error
    if progress_check == "failed":
        raise Exception("export failed")

    file_id = request_check.json()["result"]["fileId"]

    # Downloading file
    download_url = base_url + file_id + '/file'
    request_download = requests.request("GET", download_url, headers=headers, stream=True)

    # Unzipping the file --> save to raw directory/
    zipfile.ZipFile(io.BytesIO(request_download.content)).extractall(directory)
    print(survey_name + ' download complete.')

    return

# loop through surveys and download to file
for survey_name, survey_id in zip(survey_name_list, survey_id_list):
    download_qualtrics(DATA_DIR, QUALTRICS_USER, API_TOKEN, survey_id, survey_name)
