import os

from flask import Flask, request, abort

import tools

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.post("/perform_query")
def perform_query():
    json_request = request.json
    if not json_request:
        abort(400)
    user_request = tools.get_commands(json_request)

    return tools.get_result(user_request), 200


if __name__ == '__main__':
    app.run(debug=True)
