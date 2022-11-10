resource "aws_ecs_task_definition" "opensearch_project" {
  family                   = "opensearch_projecy"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 512
  memory                   = 4096

  execution_role_arn = aws_iam_role.ecs_tasks_execution_role.arn
  container_definitions    = jsonencode(
[
  {
    name = "opensearch_node1",
    image = "opensearchproject/opensearch:latest",
    cpu = 512,
    memory = 2048,
    essential = true,
    portMappings = [
        {
          containerPort = 9200
          hostPort      = 9200
        }
      ],
    logConfiguration= {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-create-group": "true",
                    "awslogs-group": "awslogs-opensearch",
                    "awslogs-region": "us-west-2",
                    "awslogs-stream-prefix": "awslogs-opensearch"
                }
            }
    environment = [
    {
      "name": "clusterName",
      "value": "opensearch-cluster"
    },
    {
      "name": "nodeName",
      "value": "opensearch_node1"
    },
    {
      "name": "discovery.seed_hosts",
      "value": "opensearch_node1"
    },

    {
      "name": "bootstrap.memory_lock",
      "value": "false"
    },
      {
      "name": "OPENSEARCH_JAVA_OPTS",
      "value": "-Xms512m -Xmx512m"
    },
      {
          "name": "discovery.type",
          "value": "single-node"
        },
      {
        "name": "DISABLE_SECURITY_PLUGIN",
        "value": "true"
      },
      {
        "name": "OPENSEARCH_PREFIX",
        "value": "plugins.security"
      },
      {
        "name": "plugins.index_state_management.enabled",
        "value": "true"
      },



  ],
    ulimits = [

        {
            "SoftLimit" : -1
            "Name": "memlock"
            "HardLimit" : -1
      },
        {
            "SoftLimit": 65536 # maximum number of open files for the OpenSearch user, set to at least 65536 on modern systems
            "Name": "nofile"
            "HardLimit": 65536
          }


    ],

  }
]
  )
  ephemeral_storage {
    size_in_gib = 30
  }

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }
}