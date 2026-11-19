# Multi-Tier Cloud Infrastructure

A containerized multi-tier web application infrastructure built using Docker, Docker Compose, Nginx, Flask, PostgreSQL, and Terraform.

The project demonstrates container orchestration, reverse proxy configuration, service communication, persistent storage, infrastructure management, and application health monitoring.

## Architecture

The application follows a three-tier architecture:

- **Presentation Layer:** Nginx acts as a reverse proxy and exposes the application on port 80.
- **Application Layer:** A Python Flask application served using Gunicorn.
- **Database Layer:** PostgreSQL provides persistent data storage.

Docker Compose manages the application containers, while Terraform manages the Docker network and PostgreSQL persistent volume.

## Technologies Used

- Docker & Docker Compose
- Terraform
- Nginx
- Python & Flask
- Gunicorn
- PostgreSQL
- Linux / Ubuntu (WSL)

## Project Structure

```text
multi-tier-cloud-infrastructure/
├── app/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── nginx/
│   └── nginx.conf
├── terraform/
│   ├── main.tf
│   ├── outputs.tf
│   ├── variables.tf
│   └── .terraform.lock.hcl
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Architecture Components

### Nginx

- Acts as a reverse proxy.
- Routes incoming HTTP requests to the Flask application.
- Uses Docker's internal DNS resolver for dynamic service-name resolution.

### Flask Application

- Runs using Gunicorn.
- Provides application health checks.
- Connects to PostgreSQL.
- Supports creating and retrieving messages through REST API endpoints.

### PostgreSQL

- Stores application messages.
- Uses a Docker named volume for persistent data storage.
- Includes a health check to verify database readiness.

### Terraform

- Uses the Docker Provider.
- Manages the Docker network.
- Manages the PostgreSQL persistent volume.
- Imports existing Docker resources into Terraform state.
- Exposes infrastructure information through Terraform outputs.
- Uses lifecycle protection to prevent accidental resource destruction.

## Prerequisites

- Docker Desktop with WSL 2 integration, or Docker Engine.
- Docker Compose.
- Terraform.
- Git.

## Running the Project

### 1. Clone the Repository

```bash
git clone https://github.com/karimabdelnab/multi-tier-cloud-infrastructure.git
cd multi-tier-cloud-infrastructure
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
DB_PASSWORD=your_secure_password
```

Do not commit the `.env` file.

### 3. Initialize Terraform

```bash
terraform -chdir=terraform init
```

### 4. Validate Terraform Configuration

```bash
terraform -chdir=terraform validate
```

### 5. Create Infrastructure on a New Environment

For a fresh environment, Terraform creates the required Docker network and PostgreSQL volume:

```bash
terraform -chdir=terraform plan
terraform -chdir=terraform apply
```

Review the execution plan and confirm when prompted.

**Note:** If the Docker network and PostgreSQL volume already exist, import them into Terraform state before managing them. Do not attempt to recreate existing resources.

### 6. Start the Application

```bash
docker compose up -d --build
```

### 7. Verify Containers

```bash
docker compose ps
```

### 8. Test the Application

```bash
curl http://localhost/
curl http://localhost/health
curl http://localhost/db-health
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Application information |
| GET | `/health` | Application health check |
| GET | `/db-health` | Database connectivity check |
| POST | `/messages` | Create a message |
| GET | `/messages` | Retrieve stored messages |

### Example Request

```bash
curl -X POST http://localhost/messages \
  -H "Content-Type: application/json" \
  -d '{"content":"Hello from Docker"}'
```

### Retrieve Messages

```bash
curl http://localhost/messages
```

## Terraform Infrastructure Management

Terraform configuration is located in the `terraform/` directory and uses the Docker Provider.

### Initialize Terraform

```bash
terraform -chdir=terraform init
```

### Validate Configuration

```bash
terraform -chdir=terraform validate
```

### Review Infrastructure Changes

```bash
terraform -chdir=terraform plan
```

### Import Existing Docker Resources

If the Docker network and PostgreSQL volume already exist, import them into Terraform state instead of recreating them:

```bash
terraform -chdir=terraform import docker_network.cloud_network <NETWORK_ID>

terraform -chdir=terraform import docker_volume.postgres_data <VOLUME_NAME>
```

Replace the placeholders with the actual Docker network ID and volume name.

### Apply Terraform Configuration

```bash
terraform -chdir=terraform apply
```

Review the execution plan before confirming.

### View Infrastructure Outputs

```bash
terraform -chdir=terraform output
```

### Important Notes

- Docker Compose manages the application containers.
- Terraform manages the Docker network and PostgreSQL persistent volume.
- The Docker network and volume are configured as external resources in Docker Compose.
- Terraform state is stored locally and excluded from Git.
- Do not delete the Terraform state file when continuing to manage existing resources.
- Lifecycle protection is configured to prevent accidental destruction of persistent infrastructure resources.

## Data Persistence

PostgreSQL data is stored in a Docker named volume, allowing database records to survive container recreation.

## Security Considerations

- Database credentials are stored in environment variables.
- `.env` is excluded from version control.
- Terraform state files are excluded from version control.
- Terraform lifecycle protection is configured for persistent infrastructure resources.

## Future Improvements

- Add CI/CD automation using GitHub Actions.
- Add automated application tests.
- Add centralized logging and monitoring.
- Deploy the infrastructure to Google Cloud Platform (GCP).
- Implement remote Terraform state management.

## Author

**Karim Abdelnaby**

Communications & Electronics Engineering Graduate | Cloud Engineer

[GitHub](https://github.com/karimabdelnab)
