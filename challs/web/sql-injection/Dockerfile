# Use an official Python runtime as a parent image
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir flask

ADD . /app

# Make port 5000 available to the outside world
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]


# docker build -t sql-injection . -f Dockerfile
# docker tag sql-injection:latest registry.ctf.secompufscar.com.br/sql-injection:latest
# docker push registry.ctf.secompufscar.com.br/sql-injection:latest
