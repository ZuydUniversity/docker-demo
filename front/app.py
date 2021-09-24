import os
import requests
from flask import Flask, abort

app = Flask(__name__)
SERV_URL = os.environ.get("SERV_URL")
if not SERV_URL:
    raise ValueError("Service URL not set")



@app.route("/")
def index():
    message = requests.get(SERV_URL)
    if message.status_code != 200:
        abort(message.status_code)
    return f"Message from service1: {message.text}"


@app.route("/serv_url")
def get_serv_url():
    return SERV_URL


@app.route("/file")
def get_file_content():
    with open("./files/test.txt") as f:
        return f.read()


if __name__ == "__main__":
    app.run()
