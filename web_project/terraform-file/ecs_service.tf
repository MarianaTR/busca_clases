resource "aws_ecs_service" "opensearch_service" {
  name            = "opensearch_service"
  cluster         = aws_ecs_cluster.ecs_cluster_project.id
  task_definition = aws_ecs_task_definition.opensearch_project.arn
  desired_count   = 1
  launch_type = "FARGATE"
  platform_version = "LATEST"
  force_new_deployment = true

  depends_on      = [aws_iam_role_policy.project_policy]
  network_configuration {
    subnets = [for subnet in aws_subnet.private_subnets : subnet.id]
    security_groups = [aws_security_group.group_security_to_aplication.id,aws_security_group.group_security_to_internet.id]
    assign_public_ip = false
  }



  load_balancer {
    target_group_arn = aws_lb_target_group.project_target_group.arn
    container_name   = "opensearch_node1"
    container_port   = 9200
  }

}