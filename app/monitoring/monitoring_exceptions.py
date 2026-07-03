class MonitoringError(Exception):
    pass


class HealthCheckError(MonitoringError):
    pass


class MetricsError(MonitoringError):
    pass


class TraceError(MonitoringError):
    pass
