resource "aws_ecr_repository" "apinine_flood" {
  name                 = "apinine_flood"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
