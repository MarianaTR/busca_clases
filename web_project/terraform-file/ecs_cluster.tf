resource "aws_kms_key" "project_key" {
  description             = "project_key"
  deletion_window_in_days = 7
}

resource "aws_cloudwatch_log_group" "cloudwatch_project" {
  name = "cloudwatch_project"
}

resource "aws_ecs_cluster" "ecs_cluster_project" {
  name = "ecs_cluster_project"

  configuration {
    execute_command_configuration {
      kms_key_id = aws_kms_key.project_key.arn
      logging    = "OVERRIDE"

      log_configuration {
        cloud_watch_encryption_enabled = true
        cloud_watch_log_group_name     = aws_cloudwatch_log_group.cloudwatch_project.name
      }
    }
  }
}