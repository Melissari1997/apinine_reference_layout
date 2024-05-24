resource "aws_cloudfront_origin_access_control" "apidoc" {
  name                              = "apidoc"
  description                       = "Access bucket ${aws_s3_bucket.apidoc.id}"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

// The Certificate is needed before this block
resource "aws_cloudfront_distribution" "apidoc" {
  origin {
    domain_name              = local.distr_domain_name
    origin_access_control_id = aws_cloudfront_origin_access_control.apidoc.id
    origin_id                = local.distr_domain_name
  }

  enabled             = true
  default_root_object = "index.html"

  is_ipv6_enabled = true

  price_class = "PriceClass_100"

  aliases = [aws_s3_bucket.apidoc.id]

  http_version = "http2"

  viewer_certificate {
    acm_certificate_arn = data.aws_acm_certificate.amazon_issued.arn

    minimum_protocol_version = "TLSv1.2_2021"
    ssl_support_method       = "sni-only"
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = local.distr_domain_name
    cache_policy_id  = data.aws_cloudfront_cache_policy.caching_disabled.id

    compress = true

    viewer_protocol_policy = "redirect-to-https"
    #min_ttl                = 0
    #default_ttl            = 3600
    #max_ttl                = 86400
  }

  restrictions {
    geo_restriction {
      locations        = []
      restriction_type = "none"
    }
  }

}
