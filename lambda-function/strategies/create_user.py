from .base import EventStrategy
from .types import EventResult


class CreateUserStrategy(EventStrategy):
    """
    Strategy for monitoring IAM user creation events.

    Tracks the creation of new IAM users to maintain security awareness
    of identity and access management changes.
    """

    def process(self, detail: dict) -> EventResult:
        """
        Process IAM user creation events.

        Extracts information about newly created IAM users and generates
        alerts to maintain visibility of identity changes.

        Args:
            detail (dict): CloudTrail event detail containing user creation info

        Returns:
            EventResult: Contains the new user's ARN and always sets alert_required
                        to True for new user creation
        """

        action_description = 'IAM User Creation'
        alert_required = True

        resource_identifier = detail.get('responseElements', {}) \
            .get('user', {}) \
            .get('arn', 'Unknown IAM user ARN')

        return EventResult(
            action_description,
            resource_identifier,
            alert_required,
        )
