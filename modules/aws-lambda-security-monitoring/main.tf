locals {
  eventbridge_rule_arn = values(module.eventbridge.eventbridge_rule_arns)[0]
  sns_topic_arn        = var.sns_topic_arn == null ? module.sns_topic[0].topic_arn : var.sns_topic_arn
}

module "sns_topic" {
  count = var.sns_topic_arn == null ? 1 : 0

  source  = "terraform-aws-modules/sns/aws"
  version = "6.1.2"

  name = var.sns_topic_name
}

module "eventbridge" {
  source  = "terraform-aws-modules/eventbridge/aws"
  version = "3.14.3"

  create_bus = false

  rules = {
    (var.eventbridge_rule_name) = {
      description = "Capture specific security-related events"
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
    (var.eventbridge_rule_name) = [
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

  function_name = var.lambda_function_name
  description   = <<-EOT
    After being triggered by an EventBridge rule, it processes specific security
    alerts and publishes them to an SNS topic.
  EOT
  handler       = "index.lambda_handler"
  runtime       = "python3.13"
  architectures = ["arm64"]

  source_path = [
    {
      path = "${path.module}/lambda-function"
      patterns = [
        "!.*/.*__pycache__.*",
        "!.*\\.DS_Store",
        "!.*requirements.*\\.txt",
      ]
    },
  ]

  environment_variables = {
    SNS_TOPIC_ARN = local.sns_topic_arn
  }

  allowed_triggers = {
    security_alerts_rule = {
      principal  = "events.amazonaws.com"
      source_arn = local.eventbridge_rule_arn
    }
  }

  attach_policy_statements = true
  policy_statements = {
    sns_topic = {
      sid       = "AllowPublishToSnsTopic"
      effect    = "Allow"
      actions   = ["sns:Publish"]
      resources = [local.sns_topic_arn]
    }
  }

  timeout = 10
}
