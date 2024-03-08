resource "aws_ecr_repository" "apinine_get_token" {
  name                 = "apinine_get_token"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
