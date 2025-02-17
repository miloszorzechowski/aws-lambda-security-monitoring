output "eventbridge_rule_arn" {
  description = "The EventBridge Rule ARN"
  value       = values(module.eventbridge.eventbridge_rule_arns)[0]
}

output "lambda_function_arn" {
  description = "The ARN of the Lambda Function"
  value       = module.lambda_function.lambda_function_arn
}

output "topic_arn" {
  description = "The ARN of the SNS topic, as a more obvious property (clone of id)"
  value       = module.sns_topic.topic_arn
}
