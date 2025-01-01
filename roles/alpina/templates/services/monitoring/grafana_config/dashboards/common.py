from attrs import define
from grafanalib.core import Template, TimeSeries, Dashboard, HIDE_VARIABLE, Target

CONF_SUPPORT_LOKI = True
CONF_SUPPORT_ZFS = True

CONF_DATASOURCE_VAR_PROM = 'prom_datasource'
CONF_DATASOURCE_VAR_LOKI = 'loki_datasource'

prom_datasource = f'${{{CONF_DATASOURCE_VAR_PROM}}}'
loki_datasource = f'${{{CONF_DATASOURCE_VAR_LOKI}}}'

prom_template = Template(
    name=CONF_DATASOURCE_VAR_PROM,
    type='datasource',
    label='Prometheus',
    query='prometheus',
    hide=HIDE_VARIABLE,
)

loki_template = Template(
    name=CONF_DATASOURCE_VAR_LOKI,
    type='datasource',
    label='Loki',
    query='loki',
    hide=HIDE_VARIABLE,
)


@define
class MyDashboard(Dashboard):
    """Wrapper class for Dashboard with some default values"""
    timezone: str = 'browser'
    sharedCrosshair: bool = True


@define
class MyTimeSeries(TimeSeries):
    """Wrapper class for TimeSeries with some default values and custom fields"""
    fillOpacity: int = 10
    lineWidth: int = 1
    showPoints: str = 'never'
    tooltipMode: str = 'multi'
    maxDataPoints: int = None

    # new fields
    axisCenteredZero: bool = False

    def to_json_data(self):
        data = super().to_json_data()
        data['fieldConfig']['defaults']['custom']['axisCenteredZero'] = self.axisCenteredZero
        return data


@define
class PromTarget(Target):
    """Wrapper class for Target with default prometheus datasource"""
    datasource: str = prom_datasource


@define
class LokiTarget(object):
    """Custom class for Loki Target, because normal Target gave errors in grafana"""
    expr: str
    legendFormat: str
    datasource: str = loki_datasource
    refId: str = None
    queryType: str = 'range'

    def to_json_data(self):
        return {
            'datasource': self.datasource,
            'expr': self.expr,
            'legendFormat': self.legendFormat,
            'refId': self.refId,
            'queryType': self.queryType,
        }


def filter_none(l: list):
    return [i for i in l if i is not None]
