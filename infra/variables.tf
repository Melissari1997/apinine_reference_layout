variable "account_role" {
  type        = string
  description = "Role to be used by Terraform to deploy the resources"
}

variable "github_oidc_provider" {
  type        = string
  description = "Arn of the OIDC provider to allow Github to use this role"
}

variable "authorizer_hasher_config" {
  type = object({
    time_cost   = optional(number, 1),
    memory_cost = optional(number, 32768),
    parallelism = optional(number, 2),
    hash_len    = optional(number, 32),
    salt_len    = optional(number, 16)
  })
  description = "Argon2id hasher configuration"
  default     = {}
}

variable "custom_domain_name" {
  type = string
}
