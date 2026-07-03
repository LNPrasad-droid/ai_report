class GISException(Exception):
    pass


class InvalidRasterError(GISException):
    pass


class UnsupportedSatelliteError(GISException):
    pass


class MissingBandError(GISException):
    pass


class RasterProcessingError(GISException):
    pass
