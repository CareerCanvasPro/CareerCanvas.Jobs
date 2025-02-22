resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "${var.cluster_name}-vpc"
  }
}

resource "aws_subnet" "private" {
  count = 2
  
  vpc_id     = aws_vpc.main.id
  cidr_block = cidrsubnet(var.vpc_cidr, 8, count.index)
  
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = {
    Name = "${var.cluster_name}-private-${count.index + 1}"
  }
}

resource "aws_subnet" "public" {
  count = 2
  
  vpc_id     = aws_vpc.main.id
  cidr_block = cidrsubnet(var.vpc_cidr, 8, count.index + 2)
  
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = {
    Name = "${var.cluster_name}-public-${count.index + 1}"
  }
}