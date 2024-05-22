resource "aws_s3_bucket" "apidoc" {
  bucket = "documentation.eoliann.solutions"
}

data "aws_iam_policy_document" "allow_cloudfront" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.apidoc.arn}/*"]
  }
}

resource "aws_s3_bucket_policy" "allow_cloudfront" {
  bucket = aws_s3_bucket.apidoc.id
  policy = data.aws_iam_policy_document.allow_cloudfront.json
}

resource "aws_s3_object" "index" {
  bucket = aws_s3_bucket.apidoc.id
  key    = "index.html"
  source = "index.html"

  etag = filemd5("./index.html")
}

/*
resource "aws_s3_bucket_website_configuration" "apidoc" {
  bucket = aws_s3_bucket.apidoc.id

  index_document {
    suffix = "index.html"
  }
}
*/

resource "aws_s3_bucket" "apidoc_log_bucket" {
  bucket = "documentation-eoliann-solutions-log-bucket"
}

resource "aws_s3_bucket_ownership_controls" "apidoc_log_bucket" {
  bucket = aws_s3_bucket.apidoc_log_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "apidoc_log_bucket" {
  depends_on = [aws_s3_bucket_ownership_controls.apidoc_log_bucket]

  bucket = aws_s3_bucket.apidoc_log_bucket.id
  acl    = "log-delivery-write"
}

resource "aws_s3_bucket_logging" "apidoc" {
  bucket = aws_s3_bucket.apidoc.id

  target_bucket = aws_s3_bucket.apidoc_log_bucket.id
  target_prefix = "log/"
}
