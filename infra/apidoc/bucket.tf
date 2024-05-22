resource "aws_s3_bucket" "apidoc" {
  bucket = "documentation.eoliann.solutions"
}

resource "aws_s3_object" "index" {
  bucket = aws_s3_bucket.apidoc.id
  key    = "index.html"
  source = "index.html"

  etag = filemd5("index.html")
}

resource "aws_s3_bucket_website_configuration" "apidoc" {
  bucket = aws_s3_bucket.apidoc.id

  index_document {
    suffix = "index.html"
  }
}
