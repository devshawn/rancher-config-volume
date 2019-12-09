FROM python:3.6-alpine

WORKDIR /

COPY setup.py /setup.py
COPY README.md /README.md
COPY ./rancher_config_volume /rancher_config_volume

RUN pip3 install -e .

ENTRYPOINT ["rancher-config-volume"]
