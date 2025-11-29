output "raw_bucket_name" {
  value = aws_s3_bucket.raw.bucket
}

output "weatherrisk_table_name" {
  value = aws_dynamodb_table.weatherrisk.name
}