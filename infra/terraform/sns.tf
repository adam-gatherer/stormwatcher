# create sns for status
resource "aws_sns_topic" "status" {
  name = "${var.project_name}-status"
}

# create sns for storm
resource "aws_sns_topic" "storm" {
  name = "${var.project_name}-storm"
}

# sns subscriptions
resource "aws_sns_topic_subscription" "status_email" {
  count = var.status_email == "" ? 0 : 1

  topic_arn = aws_sns_topic.status.arn
  protocol  = "email"
  endpoint  = var.status_email
}

resource "aws_sns_topic_subscription" "storm_email" {
  count = var.storm_email == "" ? 0 : 1

  topic_arn = aws_sns_topic.storm.arn
  protocol  = "email"
  endpoint  = var.storm_email
}
