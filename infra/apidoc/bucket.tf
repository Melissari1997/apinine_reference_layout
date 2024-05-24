resource "aws_s3_bucket" "apidoc" {
  bucket = "documentation.eoliann.solutions"
}

data "aws_iam_policy_document" "allow_cloudfront" {
  policy_id = "PolicyForCloudFrontPrivateContent"
  statement {
    sid    = "AllowCloudFrontServicePrincipal"
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.apidoc.arn}/*"]

    condition {
      test     = "StringEquals"
      variable = "AWS:SourceArn"
      values   = [aws_cloudfront_distribution.apidoc.arn]
    }
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

  content_type = "text/html"

  etag = filemd5("./index.html")
}

// FIXME: remove log bucket

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
