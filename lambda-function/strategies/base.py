from abc import ABC, abstractmethod
from .types import EventResult


class EventStrategy(ABC):
    """
    Abstract base class defining the interface for processing AWS security events.

    All concrete strategy classes must implement the process method to handle
    specific types of AWS security events.
    """

    @abstractmethod
    def process(self, detail: dict) -> EventResult:
        """
        Process the security event details and determine if an alert is required.

        Args:
            detail (dict): The 'detail' section of a CloudTrail event

        Returns:
            EventResult: The processed event results containing alert information
        """

        pass
