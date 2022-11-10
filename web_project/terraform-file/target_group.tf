
resource "aws_lb_target_group" "project_target_group" {
  name        = "project-target-group-lb-alb-tg"
  target_type = "ip"
  port        = 9200
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id

  health_check {
    enabled = "true"
    matcher = "200-399"
  }
}