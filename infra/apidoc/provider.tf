terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  required_version = "~> 1.7"
}

# Configure the AWS Provider
provider "aws" {
  region = "eu-central-1"

  default_tags {
    tags = {
      Project = "Apidoc"
    }
  }
}


// Necessary for cloudfront certificate
provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"

  default_tags {
    tags = {
      Project = "Apidoc"
    }
  }
}
