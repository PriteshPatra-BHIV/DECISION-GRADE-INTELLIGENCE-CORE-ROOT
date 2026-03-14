"""Exception hierarchy for DGIC reasoning layer."""


class ReasoningException(Exception):
    """Base exception for reasoning layer."""
    pass


class ValidationError(ReasoningException):
    """Raised when input validation fails."""
    pass


class StateError(ReasoningException):
    """Raised when state operation fails."""
    pass


class EvolutionError(ReasoningException):
    """Raised when state evolution fails."""
    pass


class InterferenceError(ReasoningException):
    """Raised when interference calculation fails."""
    pass


class CollapseError(ReasoningException):
    """Raised when collapse evaluation fails."""
    pass


class PropagationError(ReasoningException):
    """Raised when knowledge propagation fails."""
    pass


class ConfigurationError(ReasoningException):
    """Raised when configuration is invalid."""
    pass
