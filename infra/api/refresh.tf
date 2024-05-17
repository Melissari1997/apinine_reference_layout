module "gh_refresh_token" {
  source = "./modules/github_risks_role"

  role_name            = "gh_refresh_token"
  github_oidc_provider = var.github_oidc_provider
  lambda_functions_arn = ["arn:aws:lambda:eu-central-1:600920596656:function:apinine_refresh_token"]
  ecr_repositories     = [aws_ecr_repository.apinine_refresh_token.arn]
}


resource "aws_ecr_repository" "apinine_refresh_token" {
  name                 = "apinine_refresh_token"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}


module "apinine_refresh_token" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "7.2.1"

  create         = true
  create_package = false

  function_name = "apinine_refresh_token"
  description   = "This function redirects to the cognito UI login page."

  timeout     = 15
  memory_size = 256
  #ephemeral_storage_size = 1024


  attach_tracing_policy = true
  tracing_mode          = "Active"
  package_type          = "Image"
  # FIXME: possible improvements. Get latest tag from github action and inject it here (to be used with alias)
  image_uri = "${aws_ecr_repository.apinine_refresh_token.repository_url}:latest"


  environment_variables = {
    "POWERTOOLS_LOG_LEVEL" : "INFO",
    "POWERTOOLS_SERVICE_NAME" : "APININE_REFRESH_TOKEN",
    "APP_CLIENT_ID" : aws_cognito_user_pool_client.apinine_fe_client.id,
    "URL" : "https://${aws_cognito_user_pool_domain.apinine_march.domain}.auth.eu-central-1.amazoncognito.com/oauth2/token"
  }
}
