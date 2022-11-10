resource "aws_cloudwatch_log_group" "awslogs-opensearch" {
  name = "awslogs-opensearch"

  tags = {
    Environment = "production"
    Application = "serviceA"
  }
}