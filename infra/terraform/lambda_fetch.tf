# zip up the scripts
data "archive_file" "fetch_weather_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../lambdas/fetch_weather"
  output_path = "${path.module}/build/fetch_weather.zip"
}

# create iam role
resource "aws_iam_role" "lambda_fetch_weather" {
  name = "${var.project_name}-fetch-weather-role"

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
resource "aws_iam_role_policy_attachment" "lambda_fetch_weather_basic" {
  role       = aws_iam_role.lambda_fetch_weather.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# policy
resource "aws_iam_role_policy" "lambda_fetch_weather_s3" {
  name = "${var.project_name}-fetch-weather-s3"
  role = aws_iam_role.lambda_fetch_weather.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:PutObject"]
      Resource = "${aws_s3_bucket.raw.arn}/*"
    }]
  })
}

# create lambda function
resource "aws_lambda_function" "fetch_weather" {
  function_name = "${var.project_name}-fetch-weather"
  role          = aws_iam_role.lambda_fetch_weather.arn
  handler       = "handler.lambda_handler"
  runtime       = "python3.11"

  filename         = data.archive_file.fetch_weather_zip.output_path
  source_code_hash = data.archive_file.fetch_weather_zip.output_base64sha256

  timeout = 30

  environment {
    variables = {
      WEATHER_API_BASE_URL = "https://api.open-meteo.com/v1/forecast"
      LOCATION_NAME        = var.location_name
      LOCATION_LAT         = var.location_lat
      LOCATION_LON         = var.location_lon
      TIMEZONE             = var.timezone
      FORECAST_DAYS        = var.forecast_days

      RAW_BUCKET_NAME   = aws_s3_bucket.raw.bucket
      RAW_BUCKET_PREFIX = "raw/"
    }
  }

  tags = {
    Project = var.project_name
    Role    = "fetch-weather"
  }
}
