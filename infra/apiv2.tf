resource "aws_api_gateway_rest_api" "apininev2" {

  name = "apininev2_test"

  // I strongly sugget to use OpenAPI with Lambda
  body = templatefile("${path.root}/../openapi.yml.tpl", {
    invoke_arn             = "arn:aws:apigateway:eu-central-1:lambda:path/2015-03-31/functions/arn:aws:lambda:eu-central-1:600920596656:function:test/invocations"
    authorizer_credentials = module.apinine_resource_authorizer_role.role.arn
    authorizer_lambda      = module.apinine_authorizer.lambda_function_invoke_arn

    apinine_resource_drought_role = module.apinine_resource_drought_role.role.arn

    apinine_resource_flood_role = module.apinine_resource_flood_role.role.arn
    flood_lambda_uri            = module.apinine_flood.lambda_function_invoke_arn

    apinine_resource_flood_rcp85_role = module.apinine_resource_flood_rcp85_role.role.arn
    flood_rcp85_lambda_uri            = module.apinine_flood_rcp85.lambda_function_invoke_arn

    apinine_resource_wildfire_role = module.apinine_resource_wildfire_role.role.arn
    wildfire_lambda_uri            = module.apinine_wildfire.lambda_function_invoke_arn
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
module "apinine_resource_drought_role" {
  source = "./modules/apigw_resource_role"

  role_name   = "apinine_resource_drought_role"
  lambda_arns = ["arn:aws:lambda:eu-central-1:600920596656:function:test*"]
}

module "apinine_resource_wildfire_role" {
  source = "./modules/apigw_resource_role"

  role_name   = "apinine_resource_wildfire_role"
  lambda_arns = ["${module.apinine_wildfire.lambda_function_arn}*"]
}

module "apinine_resource_flood_role" {
  source = "./modules/apigw_resource_role"

  role_name   = "apinine_resource_flood_role"
  lambda_arns = ["${module.apinine_flood.lambda_function_arn}*"]
}

module "apinine_resource_flood_rcp85_role" {
  source = "./modules/apigw_resource_role"

  role_name   = "apinine_resource_flood_rcp85_role"
  lambda_arns = ["${module.apinine_flood_rcp85.lambda_function_arn}*"]
}

module "apinine_resource_authorizer_role" {
  source = "./modules/apigw_resource_role"

  role_name   = "apinine_resource_authorizer_role"
  lambda_arns = ["${module.apinine_authorizer.lambda_function_arn}*"]
}
