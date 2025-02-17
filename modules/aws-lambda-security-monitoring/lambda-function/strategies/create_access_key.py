from .base import EventStrategy
from .types import EventResult


class CreateAccessKeyStrategy(EventStrategy):
    """
    Strategy for monitoring IAM access key creation events.

    Tracks the creation of new IAM user access keys, which could indicate
    potential security risks if not properly managed.
    """

    def process(self, detail: dict) -> EventResult:
        """
        Process IAM access key creation events.

        Extracts information about newly created IAM access keys and generates
        alerts to ensure proper key management.

        Args:
            detail (dict): CloudTrail event detail containing access key creation info

        Returns:
            EventResult: Contains the new access key ID and always sets alert_required
                        to True for new key creation
        """

        action_description = 'IAM User Creating New Programmatic Access Keys'
        alert_required = True

        resource_identifier = detail.get('responseElements', {}) \
            .get('accessKey', {}) \
            .get('accessKeyId', 'Unknown access key ID')

        return EventResult(
            action_description,
            resource_identifier,
            alert_required,
        )
