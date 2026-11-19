terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 4.2"
    }
  }
}

provider "docker" {}

resource "docker_network" "cloud_network" {
  name   = "multi-tier-cloud-infrastructure_cloud-network"
  driver = "bridge"

  lifecycle {
    prevent_destroy = true
    ignore_changes  = [labels]
  }
}

resource "docker_volume" "postgres_data" {
  name   = "multi-tier-cloud-infrastructure_postgres_data"
  driver = "local"

  lifecycle {
    prevent_destroy = true
    ignore_changes  = [labels]
  }
}
