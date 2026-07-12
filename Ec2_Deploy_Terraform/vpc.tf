resource "aws_vpc" "k8_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = { Name = "K8-VPC" }
}

resource "aws_subnet" "k8_public_subnet" {
  vpc_id                  = aws_vpc.k8_vpc.id
  cidr_block              = "10.0.3.0/24"
  map_public_ip_on_launch = true
  tags = { Name = "K8-Public-Subnet" }
}

resource "aws_internet_gateway" "k8_igw" {
  vpc_id = aws_vpc.k8_vpc.id
  tags   = { Name = "K8-IGW" }
}

resource "aws_route_table" "k8_public_rt" {
  vpc_id = aws_vpc.k8_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.k8_igw.id
  }

  tags = { Name = "K8-Public-RT" }
}

resource "aws_route_table_association" "k8_public_assoc" {
  subnet_id      = aws_subnet.k8_public_subnet.id
  route_table_id = aws_route_table.k8_public_rt.id
}
