resource "aws_s3_bucket" "batch_request" {
  bucket = "apinine-batch-request"
}

resource "aws_ecr_repository" "apinine_batch_request_flood" {
  name                 = "apinine_batch_request_flood"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}


data "aws_iam_policy_document" "apinine_batch_request_flood" {
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
      "s3:GetObjectTagging",
      "s3:PutObject",
      "s3:PutObjectTagging"
    ]
    resources = [
      aws_s3_bucket.batch_request.arn,
      "${aws_s3_bucket.batch_request.arn}/*"
    ]
  }
}

data "aws_iam_policy_document" "apinine_batch_request_flood_ecr" {
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
      values   = ["arn:aws:lambda:eu-central-1:600920596656:function:apinine_batch_request_flood*"]
    }
  }
}

resource "aws_ecr_repository_policy" "apinine_batch_request_flood" {
  repository = aws_ecr_repository.apinine_batch_request_flood.name
  policy     = data.aws_iam_policy_document.apinine_batch_request_flood_ecr.json
}

module "gh_apinine_batch_request_flood" {
  source = "./modules/github_risks_role"

  role_name            = "gh_apinine_batch_request_flood"
  github_oidc_provider = var.github_oidc_provider
  lambda_functions_arn = ["arn:aws:lambda:eu-central-1:600920596656:function:apinine_batch_request_flood"]
  ecr_repositories     = [aws_ecr_repository.apinine_batch_request_flood.arn]
}

module "apinine_batch_request_flood" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "7.2.1"

  create         = true
  create_package = false

  function_name = "apinine_batch_request_flood"
  description   = "This function receives a list of locations and uploads it to an S3 bucket in CSV format."

  timeout     = 30
  memory_size = 256
  #ephemeral_storage_size = 1024

  attach_tracing_policy = true
  tracing_mode          = "Active"
  package_type          = "Image"
  # FIXME: possible improvements. Get latest tag from github action and inject it here (to be used with alias)
  image_uri = "${aws_ecr_repository.apinine_batch_request_flood.repository_url}:latest"

  attach_policy_json = true
  policy_json        = data.aws_iam_policy_document.apinine_batch_request_flood.json

  environment_variables = {
    "POWERTOOLS_LOG_LEVEL" : "INFO",
    "POWERTOOLS_SERVICE_NAME" : "APININE_BATCH_REQUEST_FLOOD",
    "S3_BUCKET_NAME" : aws_s3_bucket.batch_request.id,
    "DOMAIN_NAME" : "eoliann.testapi.solutions"
  }
}
