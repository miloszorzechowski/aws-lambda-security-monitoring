from .base import EventStrategy
from .types import EventResult


class ChangeBucketPolicyStrategy(EventStrategy):
    """
    Strategy for monitoring S3 bucket policy modifications.

    Tracks changes to S3 bucket policies, including both policy updates and deletions.
    Always generates alerts for policy changes as they may affect bucket security.
    """

    def process(self, detail: dict) -> EventResult:
        """
        Process S3 bucket policy change events.

        Extracts the affected bucket's information and generates an alert for
        any policy modification.

        Args:
            detail (dict): CloudTrail event detail containing bucket policy changes

        Returns:
            EventResult: Contains the bucket's ARN and always sets alert_required
                        to True for all policy changes
        """

        action_description = 'S3 Bucket Policy Change'
        alert_required = True

        bucket_name = detail.get('requestParameters', {}) \
            .get('bucketName')

        if bucket_name is None:
            resource_identifier = 'Unknown bucket ARN'
        else:
            resource_identifier = f'arn:aws:s3:::{bucket_name}'

        return EventResult(
            action_description,
            resource_identifier,
            alert_required,
        )
