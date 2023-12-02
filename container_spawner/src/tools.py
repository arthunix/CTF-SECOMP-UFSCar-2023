import os


def get_secret(secret_name: str, default=None, /) -> str:
    """
    Gets the docker secret from the file called f"/run/secrets/{secret_name}"
    """

    file_path = os.path.join("/run/secrets", secret_name)

    if not os.path.exists(file_path):
        return default

    with open(file_path, "r", encoding="utf-8") as secret_file:
        secret = secret_file.read().strip()

    return secret
