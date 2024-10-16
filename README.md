# FDS Qualtrics

This repository contains a Python script for downloading surveys from Qualtrics using their API. The script takes as input a directory and a CSV file containing survey names and IDs, then downloads all the surveys and saves them as CSV files to the specified directory.

## Features
- Downloads survey responses from Qualtrics in CSV format.
- Supports multiple surveys by reading a list of survey names and IDs from a CSV file.
- Automatically handles export requests and downloads files using the Qualtrics API.
- Unzips the downloaded survey data and saves it to a specified directory.

## Requirements
- Python 3.x
- Required Python packages: `requests`, `pandas`, `argparse`, `numpy`

You can install the dependencies by running:

```bash
pip install requests pandas numpy
