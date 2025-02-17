import ipaddress

from .base import EventStrategy
from .types import EventResult


class AuthorizeSecurityGroupIngressStrategy(EventStrategy):
    """
    Strategy for processing Security Group ingress rule changes.

    Analyzes changes to security group ingress rules and generates alerts
    when rules are added that allow access from non-private IP ranges.
    """

    def process(self, detail: dict) -> EventResult:
        """
        Process security group ingress rule changes and check for public access.

        Analyzes the CIDR ranges in new security group rules to determine if
        they allow access from public IP addresses.

        Args:
            detail (dict): CloudTrail event detail containing security group changes

        Returns:
            EventResult: Contains the analysis results, with alert_required set to True
                        if any rule allows access from public IP ranges
        """

        action_description = 'Security Group Ingress Rule Change (opened to non-private IP)'
        alert_required = True

        resource_identifier = detail.get('requestParameters', {}) \
            .get('groupId', 'Unknown Security Group')

        rules = detail.get('responseElements', {}) \
            .get('securityGroupRuleSet', {}) \
            .get('items', [])

        if not any(
            ipaddress.ip_network(rule.get('cidrIpv4') or rule.get('cidrIpv6')).is_global
            for rule in rules
            if rule.get('cidrIpv4') or rule.get('cidrIpv6')
        ):
            alert_required = False

        return EventResult(
            action_description,
            resource_identifier,
            alert_required,
        )
