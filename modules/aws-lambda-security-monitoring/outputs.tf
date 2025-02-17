output "eventbridge_rule_arn" {
  description = "The EventBridge rule ARN"
  value       = local.eventbridge_rule_arn
}

output "lambda_function_arn" {
  description = "The Lambda function ARN"
  value       = module.lambda_function.lambda_function_arn
}

output "sns_topic_arn" {
  description = "The SNS topic ARN"
  value       = local.sns_topic_arn
}
