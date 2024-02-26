variable "role_name" {
  type        = string
  description = "Name of the role"
}

variable "lambda_arns" {
  type        = list(string)
  description = "List of the lambda ARNs to be invoked"
}
