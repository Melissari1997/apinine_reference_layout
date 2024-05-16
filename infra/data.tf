data "aws_secretsmanager_secret" "apinine_gmaps_apikey" {
  name = "apinine/gmaps_apikey"
}

data "aws_secretsmanager_secret" "github_token_readonly" {
  name = "github_readonly"
}
