resource "aws_ecr_repository" "apinine_map_flood" {
  name                 = "apinine_map_flood"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}


data "aws_iam_policy_document" "apinine_map_flood" {
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

}

data "aws_iam_policy_document" "apinine_map_flood_ecr" {
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
      values   = ["arn:aws:lambda:eu-central-1:600920596656:function:apinine_map_flood*"]
    }
  }
}

resource "aws_ecr_repository_policy" "gh_apinine_map_flood" {
  repository = aws_ecr_repository.apinine_map_flood.name
  policy     = data.aws_iam_policy_document.apinine_map_flood_ecr.json
}

module "gh_apinine_map_flood" {
  source = "./modules/github_risks_role"

  role_name            = "gh_apinine_map_flood"
  github_oidc_provider = var.github_oidc_provider
  lambda_functions_arn = ["arn:aws:lambda:eu-central-1:600920596656:function:apinine_map_flood"]
  ecr_repositories     = [aws_ecr_repository.apinine_map_flood.arn]
}

module "apinine_map_flood" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "7.2.1"

  create         = true
  create_package = false

  function_name = "apinine_map_flood"
  description   = "This function returns the map overlay to attach to gmaps map in the ui (geojson format)."

  timeout     = 60
  memory_size = 2048
  #ephemeral_storage_size = 1024

  attach_tracing_policy = true
  tracing_mode          = "Active"
  package_type          = "Image"
  # FIXME: possible improvements. Get latest tag from github action and inject it here (to be used with alias)
  image_uri = "${aws_ecr_repository.apinine_map_flood.repository_url}:latest"

  attach_policy_json = true
  policy_json        = data.aws_iam_policy_document.apinine_map_flood.json

  environment_variables = {
    "POWERTOOLS_LOG_LEVEL" : "INFO",
    "POWERTOOLS_SERVICE_NAME" : "APININE_MAP_FLOOD"
  }
}
