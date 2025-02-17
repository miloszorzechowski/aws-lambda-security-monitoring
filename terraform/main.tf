module "sns_topic" {
  source  = "terraform-aws-modules/sns/aws"
  version = "6.1.2"

  name = "security-alerts-topic"
}

module "eventbridge" {
  source  = "terraform-aws-modules/eventbridge/aws"
  version = "3.14.3"

  create_bus = false

  rules = {
    security-alerts = {
      description = "Capture log data"
      event_pattern = jsonencode({
        "source" : [
          "aws.iam",
          "aws.s3",
          "aws.ec2"
        ],
        "detail-type" : ["AWS API Call via CloudTrail"],
        "detail" : {
          "eventSource" : [
            "iam.amazonaws.com",
            "s3.amazonaws.com",
            "ec2.amazonaws.com"
          ],
          "eventName" : [
            "CreateUser",
            "CreateAccessKey",
            "PutBucketPolicy",
            "DeleteBucketPolicy",
            "AuthorizeSecurityGroupIngress"
          ]
        }
      })
    }
  }

  targets = {
    security-alerts = [
      {
        name = "send-alerts-to-lambda-function"
        arn  = module.lambda_function.lambda_function_arn
      }
    ]
  }
}

module "lambda_function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "7.20.1"

  publish = true

  function_name = "process-security-alerts"
  description   = <<-EOT
    After being triggered by an EventBridge rule, it processes specific security
    alerts and publishes them to an SNS topic.
  EOT
  handler       = "index.lambda_handler"
  runtime       = "python3.13"
  architectures = ["arm64"]

  source_path = [
    {
      path = "../lambda-function"
      patterns = [
        "!.*/.*__pycache__.*",
        "!.*\\.DS_Store",
        "!.*requirements.*\\.txt",
      ]
    },
  ]

  environment_variables = {
    SNS_TOPIC_ARN = module.sns_topic.topic_arn
  }

  allowed_triggers = {
    security_alerts_rule = {
      principal  = "events.amazonaws.com"
      source_arn = values(module.eventbridge.eventbridge_rule_arns)[0]
    }
  }

  attach_policy_statements = true
  policy_statements = {
    sns_topic = {
      sid       = "AllowPublishToSnsTopic"
      effect    = "Allow"
      actions   = ["sns:Publish"]
      resources = [module.sns_topic.topic_arn]
    }
  }

  timeout = 10
}
