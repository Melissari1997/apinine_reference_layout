resource "aws_ecr_repository" "apinine_map_wildfire" {
  name                 = "apinine_map_wildfire"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}


data "aws_iam_policy_document" "apinine_map_wildfire" {
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

data "aws_iam_policy_document" "apinine_map_wildfire_ecr" {
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
      values   = ["arn:aws:lambda:eu-central-1:600920596656:function:apinine_map_wildfire*"]
    }
  }
}

resource "aws_ecr_repository_policy" "apinine_map_wildfire" {
  repository = aws_ecr_repository.apinine_map_wildfire.name
  policy     = data.aws_iam_policy_document.apinine_map_wildfire_ecr.json
}

module "apinine_map_wildfire" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "7.2.1"

  create         = true
  create_package = false

  function_name = "apinine_map_wildfire"
  description   = "This function performs a wildfire assessment and returns a patch of data associated with a specified layer in geojson format"

  timeout     = 60
  memory_size = 2048
  #ephemeral_storage_size = 1024

  attach_tracing_policy = true
  tracing_mode          = "Active"
  package_type          = "Image"
  # FIXME: possible improvements. Get latest tag from github action and inject it here (to be used with alias)
  image_uri = "${aws_ecr_repository.apinine_map_wildfire.repository_url}:latest"

  attach_policy_json = true
  policy_json        = data.aws_iam_policy_document.apinine_map_wildfire.json

  environment_variables = {
    "POWERTOOLS_LOG_LEVEL" : "INFO",
    "POWERTOOLS_SERVICE_NAME" : "APININE_MAP_WILDFIRE"
  }
}
