# Leyline assignment:
## Coding Challenge
Please create a REST API based on the attached OpenAPI/Swagger definition in your preferred language (Python). In addition to the endpoints included in the Swagger definition, please ensure that a Prometheus metrics endpoint is available in your application under /metrics. The application should also provide a /health endpoint.

The `/` (root) endpoint should provide the current date (UNIX epoch) and version. Additionally, a boolean property called Kubernetes should indicate if the application is running under Kubernetes. Below is an example of the expected output.

```
{
  "version": "0.1.0",
  "date": 1663534325,
  "kubernetes": false
}
```

The `/v1/tools/lookup` endpoint should resolve ONLY the IPv4 addresses for the given domain. Make sure you log all successful queries and their result in a database of your choosing (PostgreSQL, MySQL/MariaDB, MongoDB, Redis, ElasticSearch, SurrealDB, etc.). No SQLite or file-based databases, as we're planning on deploying this service to Kubernetes.

For the `/v1/tools/validate` endpoint, the service should validate if the input is an IPv4 address or not.

The `/v1/history` endpoint should retrieve the latest 20 saved queries from the database and display them in order (the most recent should be first).

Please ensure the service starts on port 3000 and your REST API has an access log. Uh-oh, don't forget about graceful shutdowns.

If possible, please make sure the OpenAPI/Swagger is available so we can generate a client for your service (not mandatory).

## Development environment

Create a fully Dockerized development environment using Docker and Docker Compose. Also, ensure all services and tools are included in the Docker Compose definition and that everything starts in the correct order and initializes correctly (migrations, etc.). We should be able to run everything with a simple:
docker-compose up -d --build
The Dockerfile and Docker Compose files should be available in the root directory of your project.

Kubernetes support
We plan on running your application in Kubernetes, so please provide either Kubernetes manifests or a Helm Chart. We prefer Helm Charts. Also, please store sensitive data in Kubernetes secrets (database passwords, etc.)

## CI Pipeline
Add a CI pipeline (GitHub Actions, GitLab CI, etc.) to test (basic tests, linting, etc.), build (Docker only), and package (Helm chart) your application upon each commit. The artifact of your build should be at least a versioned Docker image.


# Solution

This is a REST API built with FastAPI and MySQL.

## Endpoints

- `/`: Root endpoint that returns version, date, and Kubernetes status.
- `/metrics`: Prometheus metrics endpoint for scraping metrics.
- `/health`: Health check endpoint.
- `/v1/tools/lookup`: Domain lookup endpoint (IPv4 addresses only).
- `/v1/tools/validate`: IPv4 validation endpoint.
- `/v1/history`: Retrieve the latest 20 saved queries.
- `/docs`: Swagger ui endpoint.

## Running the Project

### Using Docker

1. Add all the environment variablies in the `.env` file in the root directory and add `COPY .env .env` in `Dockerfile` before the ```CMD  ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]``` in the root directory as shown below:
    ```
    MYSQL_HOST="host or ip"
    MYSQL_USER="your username"
    MYSQL_PASSWORD="your password"
    MYSQL_DB="database name (you can use "leyline_db" if you followed the instructions below in database setup section)"
    ```

2.  Build the Docker image:
    ```bash
    docker build -t leyline-assignment .
    ```

3. Run the Docker container:
    ```bash
    docker run -p 3000:3000 leyline-assignment
    ```

    *if you didn't initialize the .env file you have to run the Docker container using the command below:*

    ```bash
    docker run -p 3000:3000 \
      -e MYSQL_HOST="host or ip" \
      -e MYSQL_USER="your username" \
      -e MYSQL_PASSWORD="your password" \
      -e MYSQL_DB="database name" \
        leyline-assignment

    ```

### Running Locally

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Start the application:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 3000
    ```

## Database Setup

1. Create the MySQL database and table:

    ```sql
    CREATE DATABASE IF NOT EXISTS leyline_db;

    USE leyline_db;

    CREATE TABLE IF NOT EXISTS queries (
        id INT AUTO_INCREMENT PRIMARY KEY,
        domain VARCHAR(255) NOT NULL,
        ipv4_addresses TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ```
## Directory structure

Below is the structure of the directory for a better understanding:
```
├── Dockerfile
├── Readme.md
├── conftest.py
├── .gitignore
├── app
│   ├── database.py
│   ├── main.py
│   └── routers
│       ├── health.py
│       ├── history.py
│       ├── lookup.py
│       └── validate.py
├── leyline-assignment/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── templates/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── configmap.yaml
│   │   ├── secret.yaml
│   │   ├── hpa.yaml
│   │   └── _helpers.tpl
│   └── .helmignore
└── requirements.txt
```