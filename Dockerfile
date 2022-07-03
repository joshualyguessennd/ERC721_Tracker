# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update -q \
    && apt-get install --no-install-recommends -qy \
    gcc

# Install pip requirements
# Install linux dependencies
RUN apt-get update \
    && apt-get install -y libssl-dev npm

RUN npm install n -g \
    && npm install -g npm@latest
RUN npm install -g ganache

COPY requirements.txt .
COPY requirements-dev.txt .

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "checker.py"]
