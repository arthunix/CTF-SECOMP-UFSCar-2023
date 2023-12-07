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

# docker build -t hash-stuffing . -f Dockerfile
# docker tag hash-stuffing:latest registry.ctf.secompufscar.com.br/hash-stuffing:latest
# docker push registry.ctf.secompufscar.com.br/hash-stuffing:latest

