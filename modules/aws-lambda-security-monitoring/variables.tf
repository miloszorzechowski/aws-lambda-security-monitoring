variable "eventbridge_rule_name" {
  description = "A unique name for the EventBridge rule"
  type        = string
  default     = "security-alerts"
}

variable "lambda_function_name" {
  description = "A unique name for the Lambda function"
  type        = string
  default     = "process-security-alerts"
}

variable "sns_topic_arn" {
  description = "The ARN of the SNS topic that will be used instead of creating a new one"
  type        = string
  default     = null
}

variable "sns_topic_name" {
  description = "The name of the SNS topic to create"
  type        = string
  default     = "security-alerts-topic"
}
