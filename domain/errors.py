class DomainError(Exception):
    """Base class for domain errors."""
    pass

class OrderNotFoundError(DomainError):
    pass

class UnauthorizedAccessError(DomainError):
    pass

class InvalidReturnRequestError(DomainError):
    pass

class InvalidExchangeRequestError(DomainError):
    pass
