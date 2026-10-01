provider "aws" {
  region = "us-east-1"
}

# VPC
resource "aws_vpc" "k8_vpc" {
  cidr_block = "10.0.0.0/16"
  tags       = { Name = "K8-VPC" }
}

# Subnet
resource "aws_subnet" "k8_public_subnet" {
  vpc_id                  = aws_vpc.k8_vpc.id
  cidr_block              = "10.0.3.0/24"
  map_public_ip_on_launch = true
  tags                    = { Name = "K8-Public-Subnet" }
}

# Internet Gateway
resource "aws_internet_gateway" "k8_igw" {
  vpc_id = aws_vpc.k8_vpc.id
  tags   = { Name = "K8-IGW" }
}

# Route Table
resource "aws_route_table" "k8_public_rt" {
  vpc_id = aws_vpc.k8_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.k8_igw.id
  }

  tags = { Name = "K8-Public-RT" }
}

# Route Table Association
resource "aws_route_table_association" "k8_public_assoc" {
  subnet_id      = aws_subnet.k8_public_subnet.id
  route_table_id = aws_route_table.k8_public_rt.id
}

# Security Group
resource "aws_security_group" "k8_nginx_sg" {
  vpc_id      = aws_vpc.k8_vpc.id
  name        = "k8-nginx-sg"
  description = "Allow SSH and HTTP"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "K8-Nginx-SG" }
}


# EC2 Instance (using your AMI ID directly)
resource "aws_instance" "nginx" {
  ami                         = "ami-0e7ccba13ea56beac" # <-- replace with your AMI ID
  instance_type               = "t3.medium"
  subnet_id                   = aws_subnet.k8_public_subnet.id
  vpc_security_group_ids      = [aws_security_group.k8_nginx_sg.id]
  key_name                    = "My_new_key"
  associate_public_ip_address = true

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              amazon-linux-extras install nginx1 -y
              systemctl enable nginx
              systemctl start nginx
              echo "<h1>Hello from Nginx on Terraform EC2!</h1>" > /usr/share/nginx/html/index.html
              EOF

  tags = {
    Name = "Devops"
  }
}

# Output
output "instance_public_ip" {
  value = aws_instance.nginx.public_ip
}
