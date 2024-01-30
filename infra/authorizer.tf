resource "aws_ecr_repository" "apinine_authorizer" {
  name                 = "apinine_authorizer"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

data "aws_iam_policy_document" "apinine_authorizer_dynamo" {
  statement {
    effect = "Allow"
    actions = [
      "dynamodb:BatchGetItem",
      "dynamodb:GetItem",
      "dynamodb:PutItem",
      "dynamodb:Query",
      "dynamodb:UpdateItem"
    ]
    resources = [aws_dynamodb_table.basic-dynamodb-table.arn]
  }
}


// It is possible to add lifecyle policies
// https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecr_lifecycle_policy

module "apinine_authorizer" {
  source = "terraform-aws-modules/lambda/aws"

  create         = true
  create_package = false

  function_name = "apinine_authorizer"
  description   = "This function checks the validitity of the api key and returns the permissions associated to it."

  timeout     = 30
  memory_size = 256
  #ephemeral_storage_size = 1024


  attach_tracing_policy = true
  tracing_mode          = "Active"
  package_type          = "Image"
  image_uri             = "${aws_ecr_repository.apinine_authorizer.repository_url}:test"

  attach_policy_json = true
  policy_json        = data.aws_iam_policy_document.apinine_authorizer_dynamo.json

  environment_variables = {
    "POWERTOOLS_LOG_LEVEL" : "INFO",
    "POWERTOOLS_SERVICE_NAME" : "APININE_AUTHORIZER"
  }

}
