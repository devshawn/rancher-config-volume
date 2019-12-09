FROM python:3.6-alpine

WORKDIR /rancher

VOLUME /config

COPY setup.py /rancher/setup.py
COPY README.md /rancher/README.md
COPY ./rancher_config_volume /rancher/rancher_config_volume

RUN pip3 install -e .

ENTRYPOINT ["rancher-config-volume"]
