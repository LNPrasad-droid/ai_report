class SatelliteError(Exception):
    """Base satellite exception."""


class EarthEngineInitializationError(SatelliteError):
    pass


class InvalidAOIError(SatelliteError):
    pass


class AuthenticationError(SatelliteError):
    pass


class DatasetNotFoundError(SatelliteError):
    pass


class NoImageryFoundError(SatelliteError):
    pass


class QuotaExceededError(SatelliteError):
    pass
