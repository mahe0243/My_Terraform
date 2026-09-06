resource "aws_instance" "nginx" {
  count         = 2
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.k8_public_subnet.id
  vpc_security_group_ids = [aws_security_group.k8_sg.id]
  key_name      = var.key_name

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              amazon-linux-extras install nginx1 -y
              systemctl enable nginx
              systemctl start nginx
              echo "<h1>Hello from Nginx on Terraform EC2!</h1>" > /usr/share/nginx/html/index.html
              EOF

  tags = {
    Name        = "CICD-Master-${count.index}"
    Environment = var.environment
  }
}
