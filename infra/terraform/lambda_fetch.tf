data "archive_file" "fetch_weather_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../lambdas/fetch_weather"
  output_path = "${path.module}/build/fetch_weather.zip"
}