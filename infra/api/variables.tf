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

variable "ui_domain_name" {
  type = string
}

variable "user_db_data" {
  type = list(object({
    name            = string,
    email           = string,
    organization    = string,
    available_risks = list(string),
  }))
  description = "Temporary database collecting user information"
  default     = []
}
