# create sns for status
resource "aws_sns_topic" "status" {
    name = "${var.project_name}-status"
}

# create sns for storm
resource "aws_sns_topic" "storm" {
  name = "${var.project_name}-storm"
}

