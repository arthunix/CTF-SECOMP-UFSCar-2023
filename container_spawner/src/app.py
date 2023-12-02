import os
import subprocess
from time import sleep
from uuid import uuid4

import requests
from flask import Flask, make_response, render_template_string, request

from .redis_utils import RedisUtils
from .tools import get_secret

REGISTRY_USER = get_secret("REGISTRY_USER")
REGISTRY_PASS = get_secret("REGISTRY_PASS")

app = Flask(__name__)

container_spawn_process = subprocess.Popen(
    [
        "docker",
        "login",
        "-u",
        REGISTRY_USER,
        "-p",
        REGISTRY_PASS,
        "registry.ctf.secompufscar.com.br",
    ]
)

sleep(5)

NODE_PUB_IP = (
    requests.get("https://checkip.amazonaws.com", timeout=15)
    .content[:-1]
    .decode("utf-8")
)

DEBUG = False or os.getenv("DEBUG")

HOUR_S = 3600
HOURS_AMMMOUNT = int(os.getenv("HOURS_AMMMOUNT", "1"))
CONTAINER_TIMEOUT = HOUR_S * HOURS_AMMMOUNT

challenges = os.getenv("CHALLS").split(",")
REDIS = RedisUtils()

items_str = "".join(
    ["<option value=" + item + ">" + item + "</option>" for item in challenges]
)

COMPOSE_TEMPLATE = ""
with open("compose-template.yaml", "r", encoding="utf-8") as file:
    COMPOSE_TEMPLATE = file.read()


@app.route("/")
def form():
    return render_template_string(
        """
        <head>
            <title>chall spawner</title>
            <style>
                body {
                    background-color: black;
                    color: lime;
                    font-family: "Courier New", monospace;
                }
                
                h3 {
                    font-size: 18px;
                }
                
                p {
                    font-size: 14px;
                    margin: 0;
                    padding-left: 8px;
                }
                
                p:nth-child(odd) {
                    background-color: #0f0f0f;
                }
                
                p:nth-child(even) {
                    background-color: #151515;
                }
            </style>
        </head>
        <form method="POST" action="/process">
            Enter your groupKey: <input type="text" name="group_key">
            <select id="items" name="items">
                %s
            </select>
            <input type="submit" value="Submit">
        </form>
    """
        % (items_str)
    )


@app.route("/process", methods=["POST"])
def process():
    user_ip = request.remote_addr
    if not REDIS.valid_ip_quota_atomic(user_ip):
        return make_response("Container Quota Exceeded", 401)

    group_key = request.form.get("group_key")
    if not REDIS.check_valid_key(group_key):
        return make_response("Invalid Key", 401)

    challenge_name = request.form.get("items")

    if challenge_name not in challenges:
        return make_response("Invalid Challenge Name", 400)

    container_port = REDIS.get_next_port()

    container_id = "chall-" + str(uuid4())

    compose_text = COMPOSE_TEMPLATE

    compose_text = compose_text.format(
        container_id,
        container_id,
        challenge_name,
        CONTAINER_TIMEOUT,
        container_port,
    )

    compose_file_name = f"compose.{container_id}.yaml"
    with open(compose_file_name, "w", encoding="utf-8") as file:
        file.write(compose_text)

    # Start the 'docker stack deploy -c' command as a subprocess
    container_spawn_process = subprocess.Popen(
        # [
        #     "docker",
        #     "stack",
        #     "deploy",
        #     "-c",
        #     compose_file_name,
        #     container_id,
        # ]
        ["docker", "compose", "-f", compose_file_name, "-p", "chall", "up", "-d"]
    )

    container_spawn_process.wait()

    return render_template_string(
        # f"""
        #     <head>
        #         <title>Connect to {challenge_name} via:</title>
        #     </head>
        #     <body>
        #         <h3>The timeout is {HOURS_AMMMOUNT} hours.</h3>
        #         <p>cmd:         ssh -p {container_port} {NODE_PUB_IP}</p>
        #         <p>user:        secomp</p>
        #         <p>passwd:      secomp</p>
        #     </body>
        # """
        """
        <head>
            <title>%s chall</title>
            <style>
                body {
                    background-color: black;
                    color: lime;
                    font-family: "Courier New", monospace;
                }
                
                h3 {
                    font-size: 18px;
                }
                
                p {
                    font-size: 14px;
                    margin: 0;
                    padding-left: 8px;
                }
                
                p:nth-child(odd) {
                    background-color: #0f0f0f;
                }
                
                p:nth-child(even) {
                    background-color: #151515;
                }
            </style>
        </head>
        <body>
            <h3>The timeout is %s hour(s).</h3>
            <p>cmd:         ssh -p %s secomp@%s</p>
            <p>cmd:         ssh -p %s -o PubkeyAuthentication=no -o PreferredAuthentications=password secomp@%s</p>
            <p>NOTE:        é recomendado que o usuário troque a senha depois de logar na máquina</p>
            <p>user:        secomp</p>
            <p>passwd:      secomp</p>
        </body>
        """
        % (
            challenge_name,
            HOURS_AMMMOUNT,
            container_port,
            NODE_PUB_IP,
            container_port,
            NODE_PUB_IP,
        )
    )


if __name__ == "__main__":
    app.run(debug=bool(DEBUG), host="0.0.0.0", port=8080)
