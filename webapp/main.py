
import random

from dapr.clients import DaprClient
from flask import Flask, request, redirect


SHORT_URL_ID_LENGTH=7

DAPR_STATE_STORE="url-store"

app = Flask(__name__)
dapr = DaprClient()

@app.route("/", methods=["POST"])
def shorten():
    """Creates a shortened URL from a full URL."""
    url=request.form["url"]
    if not url:
        return redirect("/")
    short_id=generate_random_short_id()
    print("Setting", short_id, "=>", url, "...", flush=True)
    dapr.save_state(store_name=DAPR_STATE_STORE, key=short_id, value=url)
    print("Set", short_id, "=>", url, flush=True)
    short_url = request.root_url + short_id
    return f"<a href='{short_url}'>{short_url}</a>"

@app.route("/<string:short_id>")
def resolve(short_id):
    """Redirects to URL."""
    print("Resolving", short_id, "...", flush=True)
    state = dapr.get_state(store_name=DAPR_STATE_STORE, key=short_id)
    url = state.data.decode()
    print("Resolved", short_id, "=>", url, flush=True)
    return redirect(url)

@app.route("/")
def index():
    return """<form action="" method="POST">
                <input type="text" name="url" size="80">
                <input type="submit" value="Submit">
              </form>"""

def generate_random_short_id():
    return "".join(map(
        lambda i:chr(i),
        random.choices(range(65,91),
        k=SHORT_URL_ID_LENGTH)))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)