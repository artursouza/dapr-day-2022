
import random

from dapr.clients import DaprClient
from flask import Flask, request, redirect


SHORT_URL_ID_LENGTH=7

DAPR_STATE_STORE="url_store"

app = Flask(__name__)
dapr = DaprClient()

@app.route("/", methods=["POST"])
def shorten():
    """Creates a shortened URL from a full URL."""
    url=request.args.get('url')
    shortId=generateRandomShortId()
    print("Setting", shortId, "=>", url, "...", flush=True)
    dapr.save_state(store_name=DAPR_STATE_STORE, key=shortId, value=url)
    print("Set", shortId, "=>", url, flush=True)
    return str(request.root_url + shortId)

@app.route("/<string:shortId>")
def resolve(shortId):
    """Redirects to URL."""
    print("Resolving", shortId, "...", flush=True)
    state = dapr.get_state(store_name=DAPR_STATE_STORE, key=shortId)
    url = state.data.decode()
    print("Resolved", shortId, "=>", url, flush=True)
    return redirect(url)

@app.route("/")
def index():
    return "This is running!"

def generateRandomShortId():
    return "".join(map(lambda i:chr(i), random.choices(range(65,91), k=SHORT_URL_ID_LENGTH)))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)