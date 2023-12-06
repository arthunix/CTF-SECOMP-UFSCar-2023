import json
import secrets
import string
from threading import Thread
from time import sleep

from flask import Flask, make_response, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongodb:27017/myDatabase"
mongo = PyMongo(app)

TOKENS = {
    "user1": "Ye]f<n3UTt.L&a8Q[cZP2V~H`uqD9h%;kp>M}_SE",
    "user2": "xn;HF:wB(D2vkrpX+K59>fZ]T%L@7$Qa,A_!'E?j",
    "admin": "XKa+yEP~r>$}u'(6x`H7jJmS#RFh!2;?{8dfpCA.",
}


def alter_token_routine():
    global TOKENS

    char_set = string.ascii_letters + string.digits

    while True:
        for key in TOKENS:
            TOKENS[key] = "".join(secrets.choice(char_set) for _ in range(40))
        sleep(3600)


alter_token_t = Thread(target=alter_token_routine)
alter_token_t.daemon = True
alter_token_t.start()


def get_usr_from_token(token):
    for username, token_ in TOKENS.items():
        if token_ == token:
            return username

    return None


def init_db():
    users = [
        {"username": "user1", "password": "password1"},
        {"username": "user2", "password": "password2"},
        {
            "username": "admin",
            "password": "SecomPWN23{n3v3r_u$er_th3_p4$sw0rd_t0_$3ar(h}",
        },
    ]
    mongo.db.users.insert_many(users)


@app.route("/login", methods=["POST"])
def login():
    """
    curl -X POST http://localhost:8080/login -H 'Content-Type: application/json' -d '{"username":"admin","password":{"$regex":".*"}}'
    curl -X POST https://my-secure-api.ctf.secompufscar.com.br/login -H 'Content-Type: application/json' -d '{"username":"admin","password":{"$regex":".*"}}'
    """
    data = request.get_json()

    username = data["username"]
    password = data["password"]
    user = mongo.db.users.find_one({"username": username, "password": password})
    if user:
        return make_response({"authorization-token": TOKENS[username]}, 200)

    return make_response({"data": "invalid credentials"}, 401)


@app.route("/get-info")
def get_info():
    """
    curl http://localhost:8080/get-info -H 'authorization-token: Ga12GVQN4joYeR8fEiCV0hg4Wbd2vTCO95fzTyxB'
    curl https://my-secure-api.ctf.secompufscar.com.br/get-info -H 'authorization-token: Ga12GVQN4joYeR8fEiCV0hg4Wbd2vTCO95fzTyxB'
    """

    token = request.headers.get("authorization-token")

    user_name = get_usr_from_token(token)
    if user_name is None:
        return make_response(401)

    return make_response(
        {
            "userData": dict(
                mongo.db.users.find_one(
                    {"username": user_name},
                    projection={"_id": 0, "username": 1, "password": 1},
                )
            )
        },
        200,
    )


@app.route("/")
def docs():
    return open("index.html").read()


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
