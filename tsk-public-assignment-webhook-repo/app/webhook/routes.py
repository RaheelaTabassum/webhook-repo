from flask import Blueprint, json, request,jsonify,render_template
from flask import Flask
from ..extensions import get_db
from bson import ObjectId


app = Flask(__name__)

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    event_type = request.headers.get('X-GitHub-Event')
    headers = request.headers
    print(f"All headers: {headers}")
    print(f"Received event: {event_type}")
    data = request.json  # Get JSON data from the request
    print("Incoming JSON data:", data) 


    db = get_db()  # Get the MongoDB client from the extension
    collection = db['github_events']  # Use a collection named 'github_events'


    if event_type == 'pull_request':
        # Handle pull request event
        action = data['action']
        action = data['action']
        if action == 'closed' and data['pull_request']['merged']:
            pr_data = data['pull_request']
            author = pr_data['user']['login']
            from_branch = pr_data['head']['ref']  # The branch from which the PR is created
            to_branch = pr_data['base']['ref']  # The branch to which the PR is targeted
            timestamp = pr_data['merged_at']  # Use merged_at instead of created_at

            # Print merge information
            print(f"{author} merged branch {from_branch} to {to_branch} on {timestamp}  ******************************************", flush=True)
             # Prepare data to store in MongoDB
            merge_data = {
                "event_type": "pull_request_merged",
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp,
                "details": pr_data
            }
            collection.insert_one(merge_data)
        else:
            pr_data = data['pull_request']
            author = pr_data['user']['login']
            from_branch = pr_data['head']['ref']  # The branch from which the PR is created
            to_branch = pr_data['base']['ref']  # The branch to which the PR is targeted
            timestamp = pr_data['created_at']
            print(f"{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}###############################################",flush=True)
             # Prepare data to store in MongoDB
            pr_data_to_store = {
                "event_type": "pull_request",
                "action": action,
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp,
                "details": pr_data
            }

            # Insert into MongoDB
            collection.insert_one(pr_data_to_store)

    
    elif event_type == 'push':

        
        branch = data['ref'].split('/')[-1]  # Extract branch from the 'ref' field
        timestamp = data['head_commit']['timestamp']
        latest_commit_sha = data['after']

        # Check if the push event is a result of a merged pull request
        
            # Regular push
        author = data['head_commit']['author']['name']
        print(f"Author: {author} pushed to Branch: {branch} on Timestamp: {timestamp}$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ ", flush=True)
        # Prepare data to store in MongoDB
        push_data = {
            "event_type": "push",
            "author": author,
            "branch": branch,
            "timestamp": timestamp,
            "latest_commit_sha": latest_commit_sha,
            "details": data
        }

        # Insert into MongoDB
        collection.insert_one(push_data)
        # print(f"Branch: {branch}", flush=True)
        # print(f"Timestamp: {timestamp}", flush=True)
        # //{author} pushed to {to_branch} on {timestamp}  //push


    return {}, 200


@webhook.route('/')
def index():
    return render_template('index.html')    


@webhook.route('/get-events', methods=['GET'])
def get_events():
    db = get_db()
    events = list(db.github_events.find({}))  # Fetch events from your collection

    # Remove the '_id' field from each event
    for event in events:
        event.pop('_id', None)  # Remove '_id' if it exists
    
    return jsonify(events) 

# @webhook.route('/', methods=["GET"])
# def G():
#     print ("u")
#     return ("Hello World", 200)



# @app.route('/')
# def api_root():
#     print("hello world")

# @app.route('/webhook')
# def webhook():
#     print("webhook")  

                                    