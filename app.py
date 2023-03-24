import os

from flask import Flask, request, abort

import tools

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.post("/perform_query")
def perform_query():
    cmd1 = request.values.get('cmd1')
    value1 = request.values.get('value1')
    cmd2 = request.values.get('cmd2')
    value2 = request.values.get('value2')
    file_name = request.values.get('file_name')

    if None in [cmd1, cmd2, value1, value2, file_name]:
        abort(400, 'Bad keys')
    if not os.path.isfile(f'./data/{file_name}'):
        abort(400, 'Bad file_name')

    commands = ((cmd1, value1), (cmd2, value2))
    result = tools.get_result(commands, file_name)

    return result, 200


if __name__ == '__main__':
    app.run(debug=True)
