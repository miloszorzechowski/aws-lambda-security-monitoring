# AWS Security Event Monitoring

This solution provides automated monitoring and alerting for critical security events in AWS. It uses EventBridge to capture specific AWS API calls through CloudTrail and processes them using a Lambda function, which then publishes alerts to an SNS topic.

## Architecture

The solution consists of the following components:
- EventBridge Rule: Monitors specific AWS API calls related to security
- Lambda Function: Processes the security events and determines if alerts are needed
- SNS Topic: Receives and distributes security alerts

Monitored security events include:
- IAM user creation
- IAM access key creation
- S3 bucket policy modifications
- Security group ingress rule changes

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform v1.10.5 or later
- Python 3.13 or later
- Access to AWS services: Lambda, EventBridge, SNS, IAM
- S3 bucket for Terraform state (as specified in `state.tf`)

## Deployment

1. Clone the repository and navigate to the Terraform directory:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Update the following configuration files:
   - `state.tf`: Modify the S3 bucket name and profile for your environment
   - `providers.tf`: Update the AWS account ID and profile name

3. Initialize Terraform:
   ```bash
   terraform init
   ```

4. Review the planned changes:
   ```bash
   terraform plan
   ```

5. Apply the configuration:
   ```bash
   terraform validate
   terraform apply
   ```

6. Note the outputs for future reference:
   - SNS topic ARN
   - Lambda function ARN
   - EventBridge rule ARN

## Testing

You can test the solution by performing any of the monitored actions in your AWS account:

1. Create a new IAM user:
   ```bash
   aws iam create-user --user-name test-user
   ```

2. Create an access key for an IAM user:
   ```bash
   aws iam create-access-key --user-name existing-user
   ```

3. Modify a security group to allow inbound traffic:
   ```bash
   aws ec2 authorize-security-group-ingress \
     --group-id sg-xxxxx \
     --protocol tcp \
     --port 22 \
     --cidr 0.0.0.0/0
   ```

4. Modify an S3 bucket policy:
   ```bash
   aws s3api put-bucket-policy \
     --bucket your-bucket-name \
     --policy file://policy.json
   ```

After performing any of these actions, check the SNS topic for alerts. You can also monitor the Lambda function logs in CloudWatch.

## Limitations and Assumptions

1. Event Monitoring:
   - Only monitors specific security-related API calls
   - Requires CloudTrail to be enabled in the AWS account
   - Events are processed in the region where the solution is deployed

2. Lambda Function:
   - Maximum execution time is set to 10 seconds
   - Uses Python 3.13 on ARM64 architecture
   - Requires appropriate IAM permissions to publish to SNS

3. Alerting:
   - Alerts are sent only via SNS
   - No built-in alert filtering or aggregation
   - Alert format is fixed as defined in the Lambda function

4. Infrastructure:
   - Terraform state is stored in S3 and requires appropriate bucket permissions
   - AWS provider assumes specific profile and account configurations
   - Resources are created in the default region specified in the provider

## Clean Up

To remove all resources created by this solution:

```bash
terraform destroy
```

Note: This will remove all components including the Lambda function, EventBridge rule, and SNS topic. Make sure to back up any important data before proceeding.
