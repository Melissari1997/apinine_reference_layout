variable "account_role" {
  type        = string
  description = "Role to be used by Terraform to deploy the resources"
}

variable "github_oidc_provider" {
  type        = string
  description = "Arn of the IDC provider to allow Github to use this role"
}
