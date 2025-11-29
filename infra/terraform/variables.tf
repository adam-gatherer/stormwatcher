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
