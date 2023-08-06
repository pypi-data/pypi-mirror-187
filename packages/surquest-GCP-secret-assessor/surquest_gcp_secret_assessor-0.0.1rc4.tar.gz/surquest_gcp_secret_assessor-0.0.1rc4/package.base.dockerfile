FROM python:3.10-slim AS base

# Update the base image
RUN apt update && apt full-upgrade -y

# Copy local code to the container image.
ENV PROJECT_DIR /opt/project
ENV TEST_DIR /opt/project/test
ENV SRC_DIR /opt/project/src
RUN mkdir -p PROJECT_DIR
ENV HOME $PROJECT_DIR
WORKDIR $PROJECT_DIR

COPY /src/requirements.txt /tmp/app.requirements.txt

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV ENVIRONMENT dev
ENV PYTHONUNBUFFERED True
ENV PYTHONPATH="${PYTHONPATH}:${SRC_DIR}:${TEST_DIR}"

# Install python packages
RUN pip install --no-cache-dir \
    -r /tmp/app.requirements.txt

FROM base AS test

ENV ENVIRONMENT test
COPY /test/requirements.txt /tmp/test.requirements.txt
RUN pip install --no-cache-dir -r /tmp/test.requirements.txt
WORKDIR $TEST_DIR

