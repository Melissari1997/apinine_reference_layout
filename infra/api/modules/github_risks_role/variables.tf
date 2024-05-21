variable "ecr_repositories" {
  type        = list(string)
  description = "List containing the ARNs of the repositories to read from and push to."
}

variable "lambda_functions_arn" {
  type        = list(string)
  description = "List of ARNs of lambda functions to be updated (UpdateFunctionCode)."
}

variable "github_oidc_provider" {
  type        = string
  description = "Arn of the OIDC provider to allow Github to use this role"
}

variable "subject_values" {
  type        = list(string)
  default     = ["repo:eoliann-dev/*"]
  description = "List of subjects allowed to assume the role( e.g. repo:eoliann/*)."
}

variable "role_name" {
  type = string
}
