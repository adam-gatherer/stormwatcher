provider "aws" {
  region = var.aws_region
}


# random string for globally unique names
resource "random_string" "suffix" {
  length  = 6
  upper   = false
  special = false
}


# create dynamodb
resource "aws_dynamodb_table" "weatherrisk" {
  name         = "${var.project_name}-risk-db-${random_string.suffix.result}"
  billing_mode = "PAY_PER_REQUEST"

  hash_key  = "PK"
  range_key = "SK"

  attribute {
    name = "PK"
    type = "S"
  }

  attribute {
    name = "SK"
    type = "N"
  }

  tags = {
    Project = var.project_name
    Role    = "risk-store"
  }
}
