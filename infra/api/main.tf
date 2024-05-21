resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name                        = "apinine_api_key"
  billing_mode                = "PAY_PER_REQUEST"
  hash_key                    = "PK"
  range_key                   = "SK"
  deletion_protection_enabled = true

  attribute {
    name = "PK"
    type = "S"
  }

  attribute {
    name = "SK"
    type = "S"
  }

  // Global Secondary Indexes

  global_secondary_index {
    name            = "GSI1"
    hash_key        = "SK"
    range_key       = "PK"
    projection_type = "KEYS_ONLY"
  }
}
