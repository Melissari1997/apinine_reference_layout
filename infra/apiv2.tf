resource "aws_api_gateway_rest_api" "apininev2" {

  name = "apininev2_test"

  // I strongly sugget to use OpenAPI with Lambda
  body = templatefile("${path.root}/../openapi.yml.tpl", {
    invoke_arn                    = "arn:aws:apigateway:eu-central-1:lambda:path/2015-03-31/functions/arn:aws:lambda:eu-central-1:600920596656:function:test/invocations"
    authorizer_lambda             = module.apinine_authorizer.lambda_function_invoke_arn
    apinine_resource_drought_role = aws_iam_role.apinine_resource_drought_role.arn
    apinine_resource_flood_role   = aws_iam_role.apinine_resource_flood_role.arn
    #authorizer_credentials = aws_iam_role.apininev2_authorizer_invocation_role.arn
  })

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_deployment" "apinine" {
  rest_api_id = aws_api_gateway_rest_api.apininev2.id

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.apininev2.body))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "apinine" {
  deployment_id = aws_api_gateway_deployment.apinine.id
  rest_api_id   = aws_api_gateway_rest_api.apininev2.id
  stage_name    = "example"
}

resource "aws_api_gateway_method_settings" "apininev2" {
  rest_api_id = aws_api_gateway_rest_api.apininev2.id
  stage_name  = aws_api_gateway_stage.apinine.stage_name
  method_path = "*/*"

  settings {
    metrics_enabled = true
    logging_level   = "INFO" #"ERROR"
  }
}

// Resources Role
// This role will be assigned to the API resources to invoke the respective lambda functions
resource "aws_iam_role" "apinine_resource_drought_role" {
  name = "apinine_resource_drought_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "apigateway.amazonaws.com"
        }
      }
    ]
  })

  inline_policy {
    name = "drought_invoke_private_policy"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = ["lambda:InvokeFunction"]
          Resource = "arn:aws:lambda:eu-central-1:600920596656:function:test*"
          Effect   = "Allow"
        }
      ]
    })
  }
}
/*
module "apinine_resource_flood_role" {
  source = "./modules/apigw_resource_role"

  role_name   = apinine_resource_flood_role
  lambda_arns = ["arn:aws:lambda:eu-central-1:600920596656:function:test*"]
}
*/
resource "aws_iam_role" "apinine_resource_flood_role" {
  name = "apinine_resource_flood_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "apigateway.amazonaws.com"
        }
      }
    ]
  })

  inline_policy {
    name = "flood_invoke_private_policy"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = ["lambda:InvokeFunction"]
          Resource = ["arn:aws:lambda:eu-central-1:600920596656:function:test*"]
          Effect   = "Allow"
        }
      ]
    })
  }
}
