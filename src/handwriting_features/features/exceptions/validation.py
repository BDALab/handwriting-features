class FeatureNameMissingError(Exception):
    """Raised when a feature name is missing"""
    pass


class FeatureNameInvalidTypeError(Exception):
    """Raised when a feature name is of invalid type"""
    pass


class FeatureNameUnsupportedError(Exception):
    """Raised when a feature name us not supported"""
    pass


class FeatureArgumentMissingError(Exception):
    """Raised when a mandatory feature argument is missing"""
    pass


class FeatureArgumentInvalidTypeError(Exception):
    """Raised when a mandatory feature argument is of invalid type"""
    pass


class FeatureArgumentUnsupportedValueError(Exception):
    """Raised when a mandatory feature argument has unsupported value"""
    pass


class StatisticsForSingleValuedFeatureError(Exception):
    """Raised when statistics are to be computed for a single-valued feature"""
    pass
