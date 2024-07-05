from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import pytz

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['github_events']
collection = db['events']

IST = pytz.timezone('Asia/Kolkata')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    process_event(event_type, data)
    return jsonify({"message": "Event received"}), 200

def process_event(event_type, data):
    now_utc = datetime.now(pytz.utc)
    now_ist = now_utc.astimezone(IST)
    timestamp = now_ist.strftime('%I:%M:%S %p')

    if event_type == "push":
        event = {
            "author": data['pusher']['name'],
            "action": "pushed to",
            "branch": data['ref'].split('/')[-1],
            "timestamp": timestamp,
            "commit_id": data['head_commit']['id']
        }
    elif event_type == "pull_request":
        event = {
            "author": data['pull_request']['user']['login'],
            "action": "submitted a pull request from",
            "from_branch": data['pull_request']['head']['ref'],
            "to_branch": data['pull_request']['base']['ref'],
            "timestamp": timestamp,
            "request_id": data['pull_request']['id']
        }
    elif event_type == "pull_request" and data['action'] == "closed" and data['pull_request']['merged']:
        event = {
            "author": data['pull_request']['user']['login'],
            "action": "merged branch",
            "from_branch": data['pull_request']['head']['ref'],
            "to_branch": data['pull_request']['base']['ref'],
            "timestamp": timestamp,
            "request_id": data['pull_request']['id']
        }
    else:
        return
    
    collection.insert_one(event)

@app.route('/')
def index():
    events = collection.find().sort('_id', -1)
    return render_template('index.html', events=events)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
