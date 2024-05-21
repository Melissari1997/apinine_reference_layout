terraform {
  backend "s3" {
    bucket         = "terraform-be-bucket"
    key            = "apidoc/terraform.tfstate"
    region         = "eu-central-1"
    encrypt        = true
    dynamodb_table = "terraform-be-locktable"
  }
}
