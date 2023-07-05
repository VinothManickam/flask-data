from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv('.env')

app = Flask(__name__)
CORS(app)

NOTION_KEY = os.environ.get("NOTION_KEY")
NOTION_RESUME_DATABASE_ID = os.environ["NOTION_RESUME_DATABASE_ID"]

@app.route('/store_name', methods=['POST'])
def store_name():
    try:
        name = request.json['name']
    except KeyError:
        return jsonify({'error': 'Invalid request. Please provide a "name" field in the request body.'}), 400

    if not name.strip():
        return jsonify({'error': 'Invalid request. The "name" field cannot be empty.'}), 400

    notion_key = NOTION_KEY
    database_id = NOTION_RESUME_DATABASE_ID

    url = 'https://api.notion.com/v1/pages'
    headers = {
        'Authorization': f'Bearer {notion_key}',
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16'
    }
    data = {
        'parent': {'database_id': database_id},
        'properties': {
            'Name': {'title': [{'text': {'content': name}}]}
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to create entry. {str(e)}'}), 500

    return jsonify({'message': f'Successfully created entry for "{name}" in the Notion database.'}), 200

if __name__ == '__main__':
    app.run(debug=True)
