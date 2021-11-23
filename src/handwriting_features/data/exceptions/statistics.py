class UnsupportedDataForStatisticsError(Exception):
    """Raised when unsupported data are used to compute statistics"""
    pass


class StatisticsNameNotInMappingError(Exception):
    """Raised when a statistics name is not in the statistical mapping"""
    pass
