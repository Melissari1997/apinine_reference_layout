resource "aws_cognito_user_pool" "apinine_pool" {
  name = "apinine_pool"

  deletion_protection = "INACTIVE"

  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }
  auto_verified_attributes = ["email"]

  user_attribute_update_settings {
    attributes_require_verification_before_update = [
      "email",
    ]
  }

  username_attributes = [
    "email",
  ]

  email_configuration {
    email_sending_account = "COGNITO_DEFAULT"
  }

  admin_create_user_config {
    # Set to True if only the administrator is allowed to create user profiles.
    # Set to False if users can sign themselves up via an app
    allow_admin_create_user_only = true
  }

  password_policy {
    minimum_length                   = 10
    require_lowercase                = true
    require_numbers                  = true
    require_symbols                  = true
    require_uppercase                = true
    temporary_password_validity_days = 7
  }

  lifecycle {
    # We want to ignore changes relative to cognito email messages templates

    # Here we target first element of 'admin_create_user_config' which apparently is a list.
    # Otherwise, we would receive the following error:

    # │ Block type "admin_create_user_config" is represented by a list of objects, so it must be indexed using a numeric key, like
    # │ .admin_create_user_config[0].

    ignore_changes = [admin_create_user_config[0].invite_message_template]
  }
}

resource "aws_cognito_user_pool_domain" "apinine_march" {
  domain       = "apinine-march"
  user_pool_id = aws_cognito_user_pool.apinine_pool.id
}


resource "aws_cognito_user_pool_client" "apinine_fe_client" {
  name         = "apinine_fe_client"
  user_pool_id = aws_cognito_user_pool.apinine_pool.id

  access_token_validity                         = 60
  allowed_oauth_flows_user_pool_client          = true
  allowed_oauth_flows                           = ["code"]
  allowed_oauth_scopes                          = ["email", "openid"]
  auth_session_validity                         = 5
  callback_urls                                 = ["https://example.com", "http://localhost:5173/login", "https://${var.ui_domain_name}/login"]
  enable_token_revocation                       = true
  enable_propagate_additional_user_context_data = false
  explicit_auth_flows                           = ["ALLOW_REFRESH_TOKEN_AUTH", "ALLOW_USER_SRP_AUTH"]
  generate_secret                               = false
  id_token_validity                             = 60
  prevent_user_existence_errors                 = "ENABLED"
  #  read_attributes -> keep default
  refresh_token_validity       = 30
  supported_identity_providers = ["COGNITO"]
  token_validity_units {
    access_token  = "minutes"
    id_token      = "minutes"
    refresh_token = "days"
  }
  # write_attributes -> default
}
