resource "aws_ecr_repository" "apinine_flood" {
  name                 = "apinine_flood"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

data "aws_iam_policy_document" "apinine_flood" {
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

module "apinine_flood" {
  source = "terraform-aws-modules/lambda/aws"

  create         = true
  create_package = false

  function_name = "apinine_flood"
  description   = "This function returns the flood risk analysis on the provided location (address or lat and lon)."

  timeout     = 30
  memory_size = 256
  #ephemeral_storage_size = 1024


  attach_tracing_policy = true
  tracing_mode          = "Active"
  package_type          = "Image"
  image_uri             = "${aws_ecr_repository.apinine_flood.repository_url}:latest"

  attach_policy_json = true
  policy_json        = data.aws_iam_policy_document.apinine_flood.json

  environment_variables = {
    "POWERTOOLS_LOG_LEVEL" : "INFO",
    "POWERTOOLS_SERVICE_NAME" : "APININE_FLOOD"
  }

}
