output "raw_bucket_name" {
  value = aws_s3_bucket.raw.bucket
}

output "weatherrisk_table_name" {
  value = aws_dynamodb_table.weatherrisk.name
}

output "status_topic_arn" {
  value = aws_sns_topic.status.arn
}

output "storm_topic_arn" {
  value = aws_sns_topic.storm.arn
}