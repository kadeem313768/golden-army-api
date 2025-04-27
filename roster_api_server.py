from flask import Flask, jsonify
import pandas as pd
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

SERVICE_ACCOUNT_INFO = json.loads(os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON'))
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO, scopes=SCOPES
)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

SPREADSHEET_ID = '1D_r49hdJLYRm_fWGI-tWVtPEGPA8hM6eIYDC9BaLMlg'

def read_tab(range_name):
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name
    ).execute()
    values = result.get('values', [])
    if not values:
        return []
    headers = values[0]
    records = [dict(zip(headers, row)) for row in values[1:]]
    return records

@app.route('/roster', methods=['GET'])
def get_roster():
    data = read_tab('Roster!A1:Z')
    return app.response_class(
        response=json.dumps(data, indent=2, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )

@app.route('/personas', methods=['GET'])
def get_personas():
    data = read_tab('Personas!A1:Z')
    return app.response_class(
        response=json.dumps(data, indent=2, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
