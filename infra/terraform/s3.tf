resource "aws_s3_bucket" "raw" {
  bucket = "${var.project_name}-raw-json-${random_string.suffix.result}"
}

resource "aws_s3_bucket_lifecycle_configuration" "raw" {
  bucket = aws_s3_bucket.raw.id

  rule {
    id     = "expire_raw_json"
    status = "Enabled"

    filter {
      prefix = "raw/"
    }

    expiration {
      days = 90
    }
  }
}

resource "aws_lambda_permission" "allow_s3_invoke_transform" {
  statement_id  = "AllowS3InvokeTransformStore"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.transform_store.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.raw.arn
}

resource "aws_s3_bucket_notification" "raw_events" {
  bucket = aws_s3_bucket.raw.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.transform_store.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "raw/"
  }

  depends_on = [
    aws_lambda_permission.allow_s3_invoke_transform
  ]
}
