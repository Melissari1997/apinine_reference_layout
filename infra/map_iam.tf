module "gh_apinine_map_drought" {
  source = "./modules/github_risks_role"

  role_name            = "gh_apinine_map_drought"
  github_oidc_provider = var.github_oidc_provider
  lambda_functions_arn = [module.apinine_map_drought.lambda_function_arn]
  ecr_repositories     = [aws_ecr_repository.apinine_map_drought.arn]
}

module "gh_apinine_map_flood" {
  source = "./modules/github_risks_role"

  role_name            = "gh_apinine_map_flood"
  github_oidc_provider = var.github_oidc_provider
  lambda_functions_arn = [module.apinine_map_flood.lambda_function_arn]
  ecr_repositories     = [aws_ecr_repository.apinine_map_flood.arn]
}

module "gh_apinine_map_flood_rcp26" {
  source = "./modules/github_risks_role"

  role_name            = "gh_apinine_map_flood_rcp26"
  github_oidc_provider = var.github_oidc_provider
  lambda_functions_arn = [module.apinine_map_flood_rcp26.lambda_function_arn]
  ecr_repositories     = [aws_ecr_repository.apinine_map_flood_rcp26.arn]
}

module "gh_apinine_map_flood_rcp45" {
  source = "./modules/github_risks_role"

  role_name            = "gh_apinine_map_flood_rcp45"
  github_oidc_provider = var.github_oidc_provider
  lambda_functions_arn = [module.apinine_map_flood_rcp45.lambda_function_arn]
  ecr_repositories     = [aws_ecr_repository.apinine_map_flood_rcp45.arn]
}

module "gh_apinine_map_flood_rcp85" {
  source = "./modules/github_risks_role"

  role_name            = "gh_apinine_map_flood_rcp85"
  github_oidc_provider = var.github_oidc_provider
  lambda_functions_arn = [module.apinine_map_flood_rcp85.lambda_function_arn]
  ecr_repositories     = [aws_ecr_repository.apinine_map_flood_rcp85.arn]
}

module "gh_apinine_map_wildfire" {
  source = "./modules/github_risks_role"

  role_name            = "gh_apinine_map_wildfire"
  github_oidc_provider = var.github_oidc_provider
  lambda_functions_arn = [module.apinine_map_wildfire.lambda_function_arn]
  ecr_repositories     = [aws_ecr_repository.apinine_map_wildfire.arn]
}

data "aws_iam_policy_document" "gh_apinine_map_secret_iam_document" {
  statement {
    actions   = ["secretsmanager:GetSecretValue"]
    resources = [data.aws_secretsmanager_secret.github_token_readonly.arn]
  }
}

resource "aws_iam_policy" "gh_map_secret_iam_policy" {
  name   = "gh_apinine_map_secret_iam_policy"
  policy = data.aws_iam_policy_document.gh_apinine_map_secret_iam_document.json
}

resource "aws_iam_policy_attachment" "gh_map_secret_iam" {
  name = "EnableApi9MapRolesToReadGHToken"
  roles = [
    module.gh_apinine_map_flood.role.name,
    module.gh_apinine_map_flood_rcp26.role.name,
    module.gh_apinine_map_flood_rcp45.role.name,
    module.gh_apinine_map_flood_rcp85.role.name,
    module.gh_apinine_map_drought.role.name,
    module.gh_apinine_map_wildfire.role.name,
  ]
  policy_arn = aws_iam_policy.gh_map_secret_iam_policy.arn
}
