# resource "aws_ecr_repository" "apinine_user" {
#   name                 = "apinine_user"
#   image_tag_mutability = "MUTABLE"

#   image_scanning_configuration {
#     scan_on_push = true
#   }
# }

resource "aws_ssm_parameter" "user_db" {
  name  = "user_db"
  type  = "String"
  value = jsonencode(var.user_db_data)

  lifecycle {
    ignore_changes = [
      value
    ]
  }
}

# module "gh_apinine_user" {
#   source = "./modules/github_risks_role"

#   role_name            = "gh_apinine_user"
#   github_oidc_provider = var.github_oidc_provider
#   lambda_functions_arn = ["arn:aws:lambda:eu-central-1:600920596656:function:apinine_user"]
#   ecr_repositories     = [aws_ecr_repository.apinine_user.arn]
# }



data "aws_iam_policy_document" "apinine_user" {
  statement {
    effect = "Allow"
    actions = [
      "ssm:GetParameter"
    ]
    resources = [aws_ssm_parameter.user_db.arn]
  }
}

# module "apinine_user" {
#   source  = "terraform-aws-modules/lambda/aws"
#   version = "7.2.1"

#   create         = true
#   create_package = false

#   function_name = "apinine_user"
#   description   = "This function returns user information."

#   timeout     = 15
#   memory_size = 256
#   #ephemeral_storage_size = 1024

#   attach_tracing_policy = true
#   tracing_mode          = "Active"
#   package_type          = "Image"
#   # FIXME: possible improvements. Get latest tag from github action and inject it here (to be used with alias)
#   image_uri = "${aws_ecr_repository.apinine_user.repository_url}:latest"

#   attach_policy_json = true
#   policy_json        = data.aws_iam_policy_document.apinine_user.json

#   environment_variables = {
#     "POWERTOOLS_LOG_LEVEL" : "INFO",
#     "POWERTOOLS_SERVICE_NAME" : "APININE_USER",
#     "USER_DB_PARAMETER_NAME" : "user_db"
#     "URL_USERINFO" : "https://${aws_cognito_user_pool_domain.apinine_march.domain}.auth.eu-central-1.amazoncognito.com/oauth2/userinfo"
#   }
# }
