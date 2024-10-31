FROM python:3-alpine AS builder

RUN pip install grafanalib

COPY ./grafana_config/dashboards /dashboards

RUN generate-dashboards /dashboards/*.dashboard.py

FROM grafana/grafana:latest

#COPY ./grafana_config /etc/grafana
COPY ./grafana_config/dashboards/*.yaml /etc/grafana/provisioning/dashboards
COPY --from=builder /dashboards/*.json /etc/grafana/provisioning/dashboards
