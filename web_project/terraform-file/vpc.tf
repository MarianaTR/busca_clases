resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = "my_vpc_project_bc"
  }
}