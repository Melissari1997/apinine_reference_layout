resource "aws_api_gateway_rest_api" "apininev2" {

  name = "apininev2_test"

  // I strongly sugget to use OpenAPI with Lambda
  body = templatefile("${path.root}/../openapi.yml.tpl", {
    invoke_arn        = "arn:aws:apigateway:eu-central-1:lambda:path/2015-03-31/functions/arn:aws:lambda:eu-central-1:600920596656:function:test/invocations"
    authorizer_lambda = module.apinine_authorizer.lambda_function_invoke_arn
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
