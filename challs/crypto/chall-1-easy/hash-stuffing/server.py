import json
import secrets
import string

from time import sleep
from flask import Flask, make_response, request

import challenge

app = Flask(__name__)
FLAG = 'SecomPWN23{0MG,_r@ven$_4r3_$uper_|)4ng3r0u$!}'

@app.route("/", methods=["POST"])
def index():
    data = request.get_json()
    
    if('m1' not in data or 'm2' not in data):
        return make_response({"success": False, "error": "Invalid JSON", "message": "Needs m1 and m2 keys"}, 200)
    
    hash1 = challenge.cryptohash(bytes.fromhex(data['m1']))
    hash2 = challenge.cryptohash(bytes.fromhex(data['m2']))
    
    print(hash1, hash2, hash1==hash2)
    if(hash1 == hash2):
        response = {"success": True, "message": "Nice one! Here your flag: " + FLAG}
    else:
        response = {"success": False, "message": "Not this time! :P"}

    return make_response(response, 200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=13372, debug=False)
    

