from typing import NamedTuple


"""
Defines common types and data structures used across the AWS security monitoring system.

This module contains type definitions that are used to ensure consistent data structures
when processing and reporting security events.
"""

class EventResult(NamedTuple):
    """
    Contains the processed results of a security event analysis.

    This named tuple represents the standardized output format for all security
    event processing strategies. It encapsulates the essential information needed
    for security alerting and event tracking.

    Attributes:
        action_description (str): Human-readable description of the security action
                                that occurred (e.g., "IAM User Creation", "Security
                                Group Modification")
        resource_identifier (str): AWS resource identifier (e.g., ARN, ID) that
                                 uniquely identifies the affected resource
        alert_required (bool): Indicates whether this event requires an alert
                             to be sent via SNS
    """

    action_description: str
    resource_identifier: str
    alert_required: bool
