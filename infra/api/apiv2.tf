resource "aws_api_gateway_rest_api" "apininev2" {

  name = "apininev2_test"

  // I strongly sugget to use OpenAPI with Lambda
  body = local.openapi

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

// Save openapi yaml
/*
resource "local_file" "name" {
  content  = local.openapi
  filename = "../savedtest.yaml"
}
*/


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
  lambda_arns = ["${module.apinine_drought.lambda_function_arn}*"]
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

module "apinine_resource_flood_rcp45_role" {
  source = "./modules/apigw_resource_role"

  role_name   = "apinine_resource_flood_rcp45_role"
  lambda_arns = ["${module.apinine_flood_rcp45.lambda_function_arn}*"]
}

module "apinine_resource_flood_rcp26_role" {
  source = "./modules/apigw_resource_role"

  role_name   = "apinine_resource_flood_rcp26_role"
  lambda_arns = ["${module.apinine_flood_rcp26.lambda_function_arn}*"]
}

module "apinine_resource_get_token_role" {
  source = "./modules/apigw_resource_role"

  role_name   = "apinine_resource_get_token_role"
  lambda_arns = ["${module.apinine_get_token.lambda_function_arn}*"]
}

module "apinine_resource_refresh_token_role" {
  source = "./modules/apigw_resource_role"

  role_name   = "apinine_resource_refresh_token_role"
  lambda_arns = ["${module.apinine_refresh_token.lambda_function_arn}*"]
}

module "apinine_resource_cognito_login_role" {
  source = "./modules/apigw_resource_role"

  role_name   = "apinine_resource_cognito_login_role"
  lambda_arns = ["${module.apinine_cognito_login.lambda_function_arn}*"]
}

module "apinine_resource_authorizer_role" {
  source = "./modules/apigw_resource_role"

  role_name   = "apinine_resource_authorizer_role"
  lambda_arns = ["${module.apinine_authorizer.lambda_function_arn}*"]
}

module "apinine_resource_user_role" {
  source = "./modules/apigw_resource_role"

  role_name   = "apinine_resource_user_role"
  lambda_arns = ["${module.apinine_user.lambda_function_arn}*"]
}

module "apinine_resource_map_drought_role" {
  source = "./modules/apigw_resource_role"

  role_name   = "apinine_resource_map_drought_role"
  lambda_arns = ["${module.apinine_map_drought.lambda_function_arn}*"]
}

module "apinine_resource_map_flood_role" {
  source = "./modules/apigw_resource_role"

  role_name   = "apinine_resource_map_flood_role"
  lambda_arns = ["${module.apinine_map_flood.lambda_function_arn}*"]
}

module "apinine_resource_map_flood_rcp26_role" {
  source = "./modules/apigw_resource_role"

  role_name   = "apinine_resource_map_flood_rcp26_role"
  lambda_arns = ["${module.apinine_map_flood_rcp26.lambda_function_arn}*"]
}

module "apinine_resource_map_flood_rcp45_role" {
  source = "./modules/apigw_resource_role"

  role_name   = "apinine_resource_map_flood_rcp45_role"
  lambda_arns = ["${module.apinine_map_flood_rcp45.lambda_function_arn}*"]
}

module "apinine_resource_map_flood_rcp85_role" {
  source = "./modules/apigw_resource_role"

  role_name   = "apinine_resource_map_flood_rcp85_role"
  lambda_arns = ["${module.apinine_map_flood_rcp85.lambda_function_arn}*"]
}

module "apinine_resource_map_wildfire_role" {
  source = "./modules/apigw_resource_role"

  role_name   = "apinine_resource_map_wildfire_role"
  lambda_arns = ["${module.apinine_map_wildfire.lambda_function_arn}*"]
}
