variable "aws_access_key" {
  type = string
}

variable "aws_secret_key" {
  type = string
}

variable "aws_region" {
  type = string
  default = "us-west-2"
}

variable "vpc_cidr" {

  description = "CIDR range for VPC"

  type        = string

  default     = "10.0.0.0/16"

}

variable "public_subnet_cidrs" {
  type = list(string)
  description = "Public subnet CIDR values"
  default = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  type = list(string)
  description = "Private subnet CIDR values"
  default = ["10.0.3.0/24","10.0.4.0/24"]
}

variable "azs" {
  type = list(string)
  description = "Availability Zones"
  default = ["us-west-2a","us-west-2b"]
}

variable "project_env_variables" {
  default = [
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
      "name": "cluster.initial_cluster_manager_nodes",
      "value": "opensearch_node1"
    },
    {
      "name": "bootstrap.memory_lock",
      "value": "true"
    }
  ]
}