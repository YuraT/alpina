from grafanalib.core import (
    Dashboard, TimeSeries,
    Target, GridPos,
    Templating, Template, REFRESH_ON_TIME_RANGE_CHANGE, Logs
)
from grafanalib.formatunits import BYTES_IEC, SECONDS, BYTES_SEC_IEC

prom_datasource='prometheus'
loki_datasource='loki'

# TODO: this is (clown emoji), normal Target gave me errors in grafana
class LokiTarget(object):
    def to_json_data(self):
        return {
            'datasource': loki_datasource,
            'expr': '{compose_project=~"$compose_project", container_name=~"$container_name"} |= `$logs_query`',
            'legendFormat': '{{ container_name }}',
            'refId': 'A',
            'queryType': 'range',
        }

dashboard = Dashboard(
    title='Containers',
    uid='containers',
    description='Data for compose projects from default Prometheus datasource collected by Cadvisor',
    tags=[
        'example'
    ],
    templating=Templating(list=[
        Template(
            name='compose_project',
            label='Compose Project',
            dataSource=prom_datasource,
            query='label_values({__name__=~"container.*"}, container_label_com_docker_compose_project)',
            includeAll=True,
            multi=True,
            refresh=REFRESH_ON_TIME_RANGE_CHANGE,
        ),
        Template(
            name='container_name',
            label='Container',
            dataSource=prom_datasource,
            query='label_values({__name__=~"container.*", container_label_com_docker_compose_project=~"$compose_project"}, name)',
            includeAll=True,
            multi=True,
            refresh=REFRESH_ON_TIME_RANGE_CHANGE,

        ),
        Template(
            name='logs_query',
            label='Log Search',
            query='',
            type='textbox',
        ),
    ]),
    timezone='browser',
    panels=[
        TimeSeries(
            id=1,
            title='Container Memory Usage',
            unit=BYTES_IEC,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            lineWidth=2,
            fillOpacity=10,
            showPoints='never',
            stacking={'mode': 'normal'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource=prom_datasource,
                    expr='max by (name) (container_memory_usage_bytes{name=~"$container_name", container_label_com_docker_compose_project=~"$compose_project"})',
                    legendFormat='{{ name }}',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            id=2,
            title='Container CPU Usage',
            unit=SECONDS,
            gridPos=GridPos(h=8, w=12, x=12, y=0),
            lineWidth=2,
            fillOpacity=10,
            showPoints='never',
            targets=[
                Target(
                    datasource=prom_datasource,
                    expr='max by (name) (rate(container_cpu_usage_seconds_total{name=~"$container_name", container_label_com_docker_compose_project=~"$compose_project"}[$__rate_interval]))',
                    legendFormat='{{ name }}',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            id=3,
            title='Container Network Traffic',
            unit=BYTES_SEC_IEC,
            gridPos=GridPos(h=8, w=12, x=0, y=8),
            lineWidth=2,
            fillOpacity=10,
            showPoints='never',
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource=prom_datasource,
                    expr='max by (name) (rate(container_network_receive_bytes_total{name=~"$container_name", container_label_com_docker_compose_project=~"$compose_project"}[$__rate_interval]))',
                    legendFormat="rx {{ name }}",
                    refId='A',
                ),
                Target(
                    datasource=prom_datasource,
                    expr='-max by (name) (rate(container_network_transmit_bytes_total{name=~"$container_name", container_label_com_docker_compose_project=~"$compose_project"}[$__rate_interval]))',
                    legendFormat="tx {{ name }}",
                    refId='B',
                ),
            ],
        ),
        Logs(
            id=4,
            title='',
            gridPos=GridPos(h=8, w=12, x=12, y=8),
            showLabels=True,
            showCommonLabels=True,
            wrapLogMessages=True,
            prettifyLogMessage=True,
            dedupStrategy='numbers',
            targets=[
                LokiTarget(),
                # Target(
                #     datasource=loki_datasource,
                #     expr='{compose_project=~"$compose_project", container_name=~"$container_name"} |= `$logs_query`',
                #     legendFormat='{{ container_name }}',
                #     refId='A',
                # ),
            ],
        ),
    ],
).auto_panel_ids()
