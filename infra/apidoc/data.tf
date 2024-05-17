data "terraform_remote_state" "remote" {
  backend = "s3"
  config = {
    bucket = "terraform-be-bucket"
    key    = "apinine/terraform.tfstate"
    region = "your-aws-region"
  }
}
