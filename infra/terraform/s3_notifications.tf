# call on lambda
resource "aws_lambda_permission" "allow_s3_invoke_transform" {
  statement_id  = "AllowS3InvokeTransform"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.transform_store.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.raw.arn
}

# bucket notification
resource "aws_s3_bucket_notification" "raw_notifications" {
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