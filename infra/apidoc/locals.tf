locals {
  account_id = data.aws_caller_identity.current.account_id

  distr_domain_name = "${aws_s3_bucket.apidoc.id}.s3.eu-central-1.amazonaws.com"
}
