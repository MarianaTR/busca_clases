resource "aws_eip" "eip_project" {
  vpc = true

}

resource "aws_nat_gateway" "nat_gateway_project" {
  allocation_id = aws_eip.eip_project.id
  subnet_id = aws_subnet.public_subnets[0].id

  tags = {
    Name = "gw NAT"
  }
}