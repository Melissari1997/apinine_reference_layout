terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  required_version = "~> 1.6"
}

# Configure the AWS Provider
provider "aws" {
  region = "eu-central-1"
  assume_role {
    role_arn = var.account_role
  }
  default_tags {
    tags = {
      Project = "Apinine"
    }
  }
}
