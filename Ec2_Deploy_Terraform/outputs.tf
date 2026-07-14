#output "ec2_public_ip" {
#  value = aws_instance.nginx.public_ip
#}

output "public_ips" {
  value = aws_instance.nginx[*].public_ip
}

