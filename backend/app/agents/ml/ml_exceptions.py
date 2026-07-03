class MLError(Exception):
    pass


class ModelNotFoundError(MLError):
    pass


class ModelLoadError(MLError):
    pass


class PredictionError(MLError):
    pass
