# Use docker:dind as the base image
FROM docker:dind

# Install Python and pip
RUN apk add --no-cache python3 py3-pip
# RUN apt update && apt install -y python3 python3-pip

COPY ./requirements.txt .

# Install Flask
RUN pip3 install -r requirements.txt

# Copy the Flask app source code into the Docker image
COPY . .

# Run the Flask app
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]

# docker build -t container-spawner .
# docker tag container-spawner:latest registry.ctf.secompufscar.com.br/container-spawner:latest
# docker push registry.ctf.secompufscar.com.br/container-spawner:latest
