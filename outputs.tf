output "eventbridge_rule_arn" {
  description = "The EventBridge rule ARN"
  value       = module.aws_lambda_security_monitoring.eventbridge_rule_arn
}

output "lambda_function_arn" {
  description = "The Lambda function ARN"
  value       = module.aws_lambda_security_monitoring.lambda_function_arn
}

output "sns_topic_arn" {
  description = "The SNS topic ARN"
  value       = module.aws_lambda_security_monitoring.sns_topic_arn
}
