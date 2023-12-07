import json
import secrets
import string

from time import sleep
from flask import Flask, make_response, request

import challenge

app = Flask(__name__)

@app.route("/", methods=["POST"])
def index():
    """
    curl -X POST http://IP:PORT/ -H 'Content-Type: application/json' -d '{"action":"get_flag"}'
    """
    data = request.get_json()

#    if ('data' in data):
#        data['data'] = data['data'].encode('utf-8').hex()

    response = challenge.challenge(data)
    
    return make_response(response, 200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=13372, debug=False)
    

