module "gh_flood" {

  source = "./modules/github_risks_role"

  role_name            = "gh_flood"
  github_oidc_provider = var.github_oidc_provider
  lambda_functions_arn = [module.apinine_flood.lambda_function_arn, module.apinine_flood_rcp85.lambda_function_arn]
  ecr_repositories     = [aws_ecr_repository.apinine_flood.arn, aws_ecr_repository.apinine_flood_rcp85.arn]
}
