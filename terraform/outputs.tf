output "docker_network_name" {
  description = "Name of the Docker network managed by Terraform"
  value       = docker_network.cloud_network.name
}

output "docker_network_id" {
  description = "ID of the Docker network"
  value       = docker_network.cloud_network.id
}

output "postgres_volume_name" {
  description = "Name of the PostgreSQL persistent volume"
  value       = docker_volume.postgres_data.name
}
