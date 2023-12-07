FROM python:3.9-slim

# ENV

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir flask pycryptodome

# Run app.py when the container launches
CMD ["python", "server.py"]

# docker build -t gotta-go-fast . -f Dockerfile
# docker tag gotta-go-fast:latest registry.ctf.secompufscar.com.br/gotta-go-fast:latest
# docker push registry.ctf.secompufscar.com.br/gotta-go-fast:latest

