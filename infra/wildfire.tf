module "gh_wildfire" {
  source = "./modules/github_risks_role"

  role_name            = "gh_wildfire"
  github_oidc_provider = var.github_oidc_provider
  lambda_functions_arn = [module.apinine_wildfire.lambda_function_arn]
  ecr_repositories     = [aws_ecr_repository.apinine_wildfire.arn]
}

resource "aws_ecr_repository" "apinine_wildfire" {
  name                 = "apinine_wildfire"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

data "aws_iam_policy_document" "apinine_wildfire" {
  statement {
    effect = "Allow"
    actions = [
      "s3:ListAllMyBuckets",
    ]
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:GetObjectAttributes",
      "s3:GetBucketLocation",
      "s3:ListBucket",
      "s3:GetBucketVersioning",
      "s3:GetObjectTagging"
    ]
    resources = [
      "arn:aws:s3:::mlflow-monitoring",
      "arn:aws:s3:::mlflow-monitoring/*"
    ]
  }

  statement {
    effect    = "Allow"
    actions   = ["secretsmanager:GetSecretValue"]
    resources = [data.aws_secretsmanager_secret.apinine_gmaps_apikey.arn]
  }
}

module "apinine_wildfire" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "7.2.1"

  create         = true
  create_package = false

  function_name = "apinine_wildfire"
  description   = "This function returns the wildfire risk analysis on the provided location (address or lat and lon)."

  timeout     = 30
  memory_size = 2048
  #ephemeral_storage_size = 1024


  attach_tracing_policy = true
  tracing_mode          = "Active"
  package_type          = "Image"
  image_uri             = "${aws_ecr_repository.apinine_wildfire.repository_url}:latest"

  attach_policy_json = true
  policy_json        = data.aws_iam_policy_document.apinine_wildfire.json

  environment_variables = {
    "POWERTOOLS_LOG_LEVEL" : "INFO",
    "POWERTOOLS_SERVICE_NAME" : "APININE_WILDFIRE",
    "GMAPS_SECRET_NAME" : "apinine/gmaps_apikey"
  }

}
