from flask import Flask, jsonify
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

SERVICE_ACCOUNT_FILE = 'goldenarmy-dataapi-e8eb6f1f70a7.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
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
    return jsonify(data)

# Personas
@app.route('/personas', methods=['GET'])
def get_personas():
    data = read_tab('Personas!A1:Z')
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
