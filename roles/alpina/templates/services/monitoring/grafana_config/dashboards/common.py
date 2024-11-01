from grafanalib.core import Template

# TODO: consider default params for common params like line width, show points, tooltip

PrometheusTemplate = Template(
    name='datasource',
    type='datasource',
    label='Prometheus',
    query='prometheus',
)

# TODO: this slightly less (clown emoji), normal Target gave me errors in grafana
class LokiTarget(object):
    def __init__(self, loki_datasource, expr, legendFormat, refId):
        self.loki_datasource = loki_datasource
        self.expr = expr
        self.legendFormat = legendFormat
        self.refId = refId

    def to_json_data(self):
        return {
            'datasource': self.loki_datasource,
            'expr': self.expr,
            'legendFormat': self.legendFormat,
            'refId': self.refId,
            'queryType': 'range',
        }
