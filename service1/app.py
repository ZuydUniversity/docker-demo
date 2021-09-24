import os
from flask import Flask

app = Flask(__name__)
MESSAGE = os.environ.get("MESSAGE") or "Default message"


@app.route("/")
def index():
    return MESSAGE


if __name__ == "__main__":
    app.run()
