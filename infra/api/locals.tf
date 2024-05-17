locals {
  openapi = templatefile("${path.root}/../../openapi.yml.tpl", {
    domain_name = var.custom_domain_name

    authorizer_credentials = module.apinine_resource_authorizer_role.role.arn
    authorizer_lambda      = module.apinine_authorizer.lambda_function_invoke_arn

    apinine_resource_drought_role = module.apinine_resource_drought_role.role.arn
    drought_lambda_uri            = module.apinine_drought.lambda_function_invoke_arn

    apinine_resource_flood_role = module.apinine_resource_flood_role.role.arn
    flood_lambda_uri            = module.apinine_flood.lambda_function_invoke_arn

    apinine_resource_flood_rcp85_role = module.apinine_resource_flood_rcp85_role.role.arn
    flood_rcp85_lambda_uri            = module.apinine_flood_rcp85.lambda_function_invoke_arn

    apinine_resource_flood_rcp45_role = module.apinine_resource_flood_rcp45_role.role.arn
    flood_rcp45_lambda_uri            = module.apinine_flood_rcp45.lambda_function_invoke_arn

    apinine_resource_flood_rcp26_role = module.apinine_resource_flood_rcp26_role.role.arn
    flood_rcp26_lambda_uri            = module.apinine_flood_rcp26.lambda_function_invoke_arn

    apinine_resource_wildfire_role = module.apinine_resource_wildfire_role.role.arn
    wildfire_lambda_uri            = module.apinine_wildfire.lambda_function_invoke_arn

    apinine_resource_get_token_role = module.apinine_resource_get_token_role.role.arn
    get_token_lambda_uri            = module.apinine_get_token.lambda_function_invoke_arn

    apinine_resource_cognito_login_role = module.apinine_resource_cognito_login_role.role.arn
    cognito_login_lambda_uri            = module.apinine_cognito_login.lambda_function_invoke_arn

    apinine_resource_refresh_token_role = module.apinine_resource_refresh_token_role.role.arn
    refresh_token_lambda_uri            = module.apinine_refresh_token.lambda_function_invoke_arn

    apinine_resource_user_role = module.apinine_resource_user_role.role.arn
    user_lambda_uri            = module.apinine_user.lambda_function_invoke_arn

    apinine_resource_map_drought_role = module.apinine_resource_map_drought_role.role.arn
    map_drought_lambda_uri            = module.apinine_map_drought.lambda_function_invoke_arn

    apinine_resource_map_flood_role = module.apinine_resource_map_flood_role.role.arn
    map_flood_lambda_uri            = module.apinine_map_flood.lambda_function_invoke_arn

    apinine_resource_map_flood_rcp26_role = module.apinine_resource_map_flood_rcp26_role.role.arn
    map_flood_rcp26_lambda_uri            = module.apinine_map_flood_rcp26.lambda_function_invoke_arn

    apinine_resource_map_flood_rcp45_role = module.apinine_resource_map_flood_rcp45_role.role.arn
    map_flood_rcp45_lambda_uri            = module.apinine_map_flood_rcp45.lambda_function_invoke_arn

    apinine_resource_map_flood_rcp85_role = module.apinine_resource_map_flood_rcp85_role.role.arn
    map_flood_rcp85_lambda_uri            = module.apinine_map_flood_rcp85.lambda_function_invoke_arn

    apinine_resource_map_wildfire_role = module.apinine_resource_map_wildfire_role.role.arn
    map_wildfire_lambda_uri            = module.apinine_map_wildfire.lambda_function_invoke_arn

    apinine_user_pool = aws_cognito_user_pool.apinine_pool.arn
  })
}
