FROM python:3-alpine AS builder

RUN pip install grafanalib

COPY ./grafana_config/dashboards /dashboards

# Required for grafanalib to find the shared python files like common.py
# https://github.com/weaveworks/grafanalib/issues/58
ENV PYTHONPATH=/dashboards

RUN generate-dashboards /dashboards/*.dashboard.py

FROM grafana/grafana:latest

#COPY ./grafana_config /etc/grafana
COPY ./grafana_config/dashboards/*.yaml /etc/grafana/provisioning/dashboards
COPY --from=builder /dashboards/*.json /etc/grafana/provisioning/dashboards
