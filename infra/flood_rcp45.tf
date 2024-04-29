resource "aws_ecr_repository" "apinine_flood_rcp45" {
  name                 = "apinine_flood_rcp45"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}


data "aws_iam_policy_document" "apinine_flood_rcp45" {
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

data "aws_iam_policy_document" "apinine_flood_rcp45_ecr" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = [
      "ecr:BatchGetImage",
      "ecr:GetDownloadUrlForLayer",
      "ecr:GetRepositoryPolicy",
      "ecr:SetRepositoryPolicy"
    ]

    condition {
      test     = "StringLike"
      variable = "aws:sourceArn"
      values   = ["arn:aws:lambda:eu-central-1:600920596656:function:apinine_flood_rcp45*"]
    }
  }
}

resource "aws_ecr_repository_policy" "gh_apinine_flood_rcp45" {
  repository = aws_ecr_repository.apinine_flood_rcp45.name
  policy     = data.aws_iam_policy_document.apinine_flood_rcp45_ecr.json
}

module "gh_apinine_flood_rcp45" {
  source = "./modules/github_risks_role"

  role_name            = "gh_apinine_flood_rcp45"
  github_oidc_provider = var.github_oidc_provider
  lambda_functions_arn = ["arn:aws:lambda:eu-central-1:600920596656:function:apinine_flood_rcp45"]
  ecr_repositories     = [aws_ecr_repository.apinine_flood_rcp45.arn]
}

module "apinine_flood_rcp45" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "7.2.1"

  create         = true
  create_package = false

  function_name = "apinine_flood_rcp45"
  description   = "This function returns the flood risk analysis on the provided location for rcp 8.5 (address or lat and lon)."

  timeout     = 15
  memory_size = 256
  #ephemeral_storage_size = 1024

  attach_tracing_policy = true
  tracing_mode          = "Active"
  package_type          = "Image"
  # FIXME: possible improvements. Get latest tag from github action and inject it here (to be used with alias)
  image_uri = "${aws_ecr_repository.apinine_flood_rcp45.repository_url}:latest"

  attach_policy_json = true
  policy_json        = data.aws_iam_policy_document.apinine_flood_rcp45.json

  environment_variables = {
    "POWERTOOLS_LOG_LEVEL" : "INFO",
    "POWERTOOLS_SERVICE_NAME" : "APININE_FLOOD_RCP85",
    "GMAPS_SECRET_NAME" : "apinine/gmaps_apikey"
  }
}
