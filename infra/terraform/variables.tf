variable "aws_region" {
  type        = string
  description = "AWS region to deploy Stormwatch into"
}

variable "project_name" {
  type        = string
  description = "Name prefix for Stormwatch resources"
}

variable "location_name" {
  type        = string
  description = "Human readable name for the location"
}

variable "location_lat" {
  type = string
}

variable "location_lon" {
  type = string
}

variable "timezone" {
  type        = string
  description = "Time zone for API call"
}

variable "forecast_days" {
  type        = string
  description = "Number of days to fetch weather forecast for"
}

variable "storm_threshold" {
  type        = string
  description = "Risk score threshold for 'storm incoming' notifications"
}

# sns subscriptions
variable "status_email" {
  type        = string
  description = "Email address for write success/failure notifications"
}

variable "storm_email" {
  type        = string
  description = "Email address for 'storm incoming' alerts"
}