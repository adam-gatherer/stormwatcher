terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "random_string" "suffix" {
  length  = 6
  upper   = false
  special = false
}

resource "aws_s3_bucket" "raw" {
  bucket = "${var.project_name}-raw-json-${random_string.suffix.result}"

  tags = {
    Project = var.project_name
    Role    = "raw-json-landing"
  }
}