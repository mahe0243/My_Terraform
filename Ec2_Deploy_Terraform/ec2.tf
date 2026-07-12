# Fetch latest Amazon Linux 2 AMI dynamically
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-kernel-5.10-hvm-*-x86_64-gp2"]
  }
}

resource "aws_instance" "nginx" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.k8_public_subnet.id
  vpc_security_group_ids = [aws_security_group.k8_nginx_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              amazon-linux-extras install nginx1 -y
              systemctl enable nginx
              systemctl start nginx
              echo "<h1>Hello from Nginx on Terraform EC2!</h1>" > /usr/share/nginx/html/index.html
              EOF

  tags = { Name = "Terraform-Nginx" }
}
