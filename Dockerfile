FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y libpq-dev gcc python3.8-dev

#================================================================
# pip install required modules
#================================================================

RUN pip install --upgrade setuptools pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

#==================================================
# Copy the latest code
#==================================================

RUN mkdir -p /kodo-app
WORKDIR /kodo-app
COPY . /kodo-app

# Expose server port
EXPOSE 9000

CMD /bin/bash run.sh