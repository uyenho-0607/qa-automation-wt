from src.utils import DotDict


class BaseObject(DotDict):
    """Base class for all objects with common functionality."""

    def __init__(self, **kwargs):
        """Initialize the base object with any provided attributes."""
        super().__init__()
        self._update_attributes(**kwargs)

    def _update_attributes(self, **kwargs):
        """Update object attributes dynamically.
        Args:
            **kwargs: Any attributes to update
        """
        for key, value in kwargs.items():
            self[key] = value
        return self

    def to_dict(self) -> DotDict:
        """Convert the account object to a dictionary containing all attributes."""
        # Since we inherit from DotDict, we can return a filtered version of self
        return DotDict({k: v for k, v in self.items() if v is not None and not k.startswith('_')})
