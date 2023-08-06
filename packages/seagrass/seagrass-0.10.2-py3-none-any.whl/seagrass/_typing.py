# flake8: noqa: F401

# Type annotations for Seagrass
# Seagrass code should import type annotations from this module rather
# than from `typing` to ensure version compatibility

from typing import *

# The __all__ list includes all of the attributes of typing that were
# brought into scope.
import typing as _t

__all__: List[str] = []
__all__ += _t.__all__  # type: ignore[attr-defined]

# Import additional attributes for Python < 3.8
_extended_attrs = ["Final", "Literal", "Protocol", "runtime_checkable"]

# Additional types for Seagrass:
class Missing:
    """Unique type used throughout Seagrass to represent a missing value."""

    __slots__: List[str] = []

    def __repr__(self) -> str:
        return f"<{__name__}.{self.__class__.__name__}>"


MISSING: Final[Missing] = Missing()

_T = TypeVar("_T")

# Maybe[T] is a type that represents a value that is potentially missing its value.
# This is distinct from Optional[T], which represents a value that could have type
# T or that could be None. In cases where a None value should be allowed, this type
# may be used instead.
Maybe = Union[_T, Missing]

_R = TypeVar("_R")
_F = TypeVar("_F", bound=Callable)
_FR = TypeVar("_FR", bound=Callable[..., _R])


class AuditedFunc(Protocol[_FR]):

    __event_name__: str

    def __call__(*args, **kwargs) -> _R:    # type: ignore[type-var]
        ...


class AuditDecorator(Protocol):
    def __call__(self, func: _F) -> _F:
        ...


# Add additional types to the __all__ list:

__all__ += [
    "Missing",
    "MISSING",
    "Maybe",
    "AuditedFunc",
    "AuditDecorator",
]

__all__ = sorted(__all__)
