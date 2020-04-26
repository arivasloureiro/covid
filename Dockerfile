FROM debian:buster

ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV FLASK_HOST=0.0.0.0
ENV PORT=5000

ADD . /opt

RUN apt update && apt install -y --no-install-recommends \
    xvfb ca-certificates python3 python3-tk python3-distutils curl &&\
    rm -rf /var/lib/apt/lists

RUN cd /opt && \
    curl -sLk https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py && rm get-pip.py && \
    pip3 install setuptools && \
    pip3 install -r requirements.txt

WORKDIR /opt
EXPOSE ${PORT}
ENTRYPOINT flask run --host=${FLASK_HOST} --port=${PORT}


