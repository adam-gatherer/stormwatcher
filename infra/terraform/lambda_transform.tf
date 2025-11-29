# zip up the scripts
data "archive_file" "transform_store_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../lambdas/transform_store"
  output_path = "${path.module}/build/transform_store.zip"
}

# create iam role
resource "aws_iam_role" "lambda_transform_store" {
  name = "${var.project_name}-transform-store-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

# attach policy
resource "aws_iam_role_policy_attachment" "lambda_transform_store_basic" {
  role       = aws_iam_role.lambda_transform_store.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# policy
resource "aws_iam_role_policy" "lambda_transform_store_s3_dynamo" {
  name = "${var.project_name}-transform-store-s3-dynamo"
  role = aws_iam_role.lambda_transform_store.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject"]
        Resource = "${aws_s3_bucket.raw.arn}/*"
      },
      {
        Effect   = "Allow"
        Action   = ["dynamodb:PutItem"]
        Resource = aws_dynamodb_table.weatherrisk.arn
      }
    ]
  })
}

# create lambda function
resource "aws_lambda_function" "transform_store" {
  function_name = "${var.project_name}-transform-store"
  role          = aws_iam_role.lambda_transform_store.arn
  handler       = "handler.lambda_handler"
  runtime       = "python3.11"

  filename         = data.archive_file.transform_store_zip.output_path
  source_code_hash = data.archive_file.transform_store_zip.output_base64sha256

  timeout = 30

  environment {
    variables = {
      WEATHERRISK_TABLE_NAME = aws_dynamodb_table.weatherrisk.name
    }
  }

  tags = {
    Project = var.project_name
    Role    = "transform-store"
  }
}