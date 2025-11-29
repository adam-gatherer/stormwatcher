# create schedule
resource "aws_cloudwatch_event_rule" "fetch_schedule" {
  name                = "${var.project_name}-fetch-0600"
  schedule_expression = "cron(0 6 * * ? *)"
}


# target lambda
resource "aws_cloudwatch_event_target" "fetch_target" {
  rule      = aws_cloudwatch_event_rule.fetch_schedule.name
  target_id = "fetch-weather-lambda"
  arn       = aws_lambda_function.fetch_weather.arn

  depends_on = [
    aws_lambda_function.fetch_weather
  ]
}


# permissions
resource "aws_lambda_permission" "allow_eventbridge_invoke_fetch" {
  statement_id  = "AllowEventBridgeInvokeFetch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.fetch_weather.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.fetch_schedule.arn
}

