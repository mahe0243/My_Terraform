provider "aws" {
  region = var.region
}

variable "region" {
  description = "AWS region"
  type        = string
}

variable "key_name" {
  description = "SSH key name"
  type        = string
  default     = "My_new_key"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
}

variable "environment" {
  description = "Environment name (dev, qa, prod)"
  type        = string
}

data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-kernel-5.10-hvm-*-x86_64-gp2"]
  }
}
