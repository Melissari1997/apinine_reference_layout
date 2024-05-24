data "aws_caller_identity" "current" {}

data "aws_cloudfront_cache_policy" "caching_disabled" {
  name = "Managed-CachingDisabled"
}

data "aws_acm_certificate" "amazon_issued" {
  provider = aws.us_east_1

  domain      = aws_s3_bucket.apidoc.id
  types       = ["AMAZON_ISSUED"]
  most_recent = true
}
