import json
import os

import boto3
from botocore.exceptions import ClientError

from strategies import (
    AuthorizeSecurityGroupIngressStrategy,
    ChangeBucketPolicyStrategy,
    CreateAccessKeyStrategy,
    CreateUserStrategy,
)

sns_topic_arn = os.getenv('SNS_TOPIC_ARN')
if sns_topic_arn is None:
    print('SNS_TOPIC_ARN environment variable is not specified')

sns_client = boto3.client('sns')

strategy_map = {
    'AuthorizeSecurityGroupIngress': AuthorizeSecurityGroupIngressStrategy(),
    'CreateAccessKey': CreateAccessKeyStrategy(),
    'CreateUser': CreateUserStrategy(),
    'DeleteBucketPolicy': ChangeBucketPolicyStrategy(),
    'PutBucketPolicy': ChangeBucketPolicyStrategy(),
}


def lambda_handler(event, context): # pylint: disable=unused-argument
    """
    AWS Lambda handler that processes CloudTrail security events and sends notifications.

    Monitors specific AWS security-related events and publishes alerts to an SNS topic
    when critical changes are detected. Supported events include security group modifications,
    IAM user creation, access key creation, and S3 bucket policy changes.

    Args:
        event (dict): CloudTrail event data containing security event details
        context (LambdaContext): AWS Lambda context object (unused)

    Returns:
        None

    Environment Variables:
        SNS_TOPIC_ARN (str): ARN of the SNS topic for publishing security alerts
    """

    print('Received event:', json.dumps(event))

    detail = event.get('detail', {})
    event_name = detail.get('eventName', 'Unknown')
    event_time = detail.get('eventTime', 'Unknown time')
    initiator = detail.get('userIdentity', {}).get('arn', 'Unknown initiator')

    if event_name not in strategy_map:
        print('Unsupported event:', event_name)
        print('Interrupting...')
        return

    strategy = strategy_map.get(event_name)

    (
        action_description,
        resource_identifier,
        alert_required,
    ) = strategy.process(detail)

    if not alert_required:
        print("No critical changes, alert is not published")
        print("Aborting...")
        return

    message = json.dumps({
        'time': event_time,
        'resource': resource_identifier,
        'initiator': initiator,
        'action': action_description,
    })

    print('Publishing alert to SNS:', message)

    try:
        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject='ALERT: AWS Security Event Notification',
        )
        print('SNS publish response:', json.dumps(response))
    except ClientError as e:
        print('Error publishing SNS message:', e)
