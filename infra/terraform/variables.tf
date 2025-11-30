variable "aws_region" {
  type        = string
  description = "AWS region to deploy Stormwatch into"
  default     = "eu-west-1"
}

variable "project_name" {
  type        = string
  description = "Name prefix for Stormwatch resources"
  default     = "stormwatch"
}

variable "location_name" {
  type        = string
  description = "Human readable name for the location"
  default     = "Edinburgh"
}

variable "location_lat" {
  type        = string
  default     = "55.9486"
}

variable "location_lon" {
  type        = string
  default     = "-3.1999"
}

variable "timezone" {
  type        = string
  description = "Time zone for API call"
  default     = "Europe/London"
}

variable "forecast_days" {
  type        = string
  description = "Number of days to fetch weather forecast for"
  default     = "1"
}

variable "storm_threshold" {
  type        = string
  description = "Risk score threshold for 'storm incoming' notifications"
  default     = "0.8"
}