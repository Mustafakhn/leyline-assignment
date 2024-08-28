# Leyline assignment:
[Assignment ](https://m3d60c6dc7z.larksuite.com/docx/Kw8zdbAAMotF42xyJhcunL1Dsvf)
# Solution
This is a REST API Application that i built with FastAPI and MySQL.

Below i have mentioned the details of the application and the steps to run the application in various environments such as:
- Locallly
- Docker (Using Dockerfile or docker-compose file)
- Kubernetes (k8s) - (Using helm charts)

## Endpoints

Below are the endpoints of the application:

- `/`: Root endpoint that returns version, date, and Kubernetes status.
- `/metrics`: Prometheus metrics endpoint for scraping metrics.
- `/health`: Health check endpoint.
- `/v1/tools/lookup`: Domain lookup endpoint (IPv4 addresses only).
- `/v1/tools/validate`: IPv4 validation endpoint.
- `/v1/history`: Retrieve the latest 20 saved queries.
- `/docs`: Swagger ui endpoint.

## Running the Project

### Using Docker with Dockerfile

1. Add all the environment variablies in the `.env` file in the root directory and add `COPY .env .env` in `Dockerfile` before the ```CMD  ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]``` in the root directory as shown below:
    ```
    MYSQL_HOST="host or ip"
    MYSQL_USER="your username"
    MYSQL_PASSWORD="your password"
    MYSQL_DB="leyline_db"
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
### Using Docker with docker compose

1. Run the following command in the root directory of the project:
    ```bash
    docker-compose up -d --build
    ```
2. To stop the containers, run:
    ```bash
    docker-compose down
    ```

### Deploying to Kubernetes using Helm

1. Ensure you have Helm installed and your kubectl is configured to connect to your Kubernetes cluster.

2. Navigate to the directory containing the Helm chart (assuming it's in a directory named `leyline-assignment-chart`):
    ```bash
    cd leyline-assignment-chart
    ```

3. Update the `values.yaml` file with your specific configuration, such as the Docker `image repository` and tag, database details (which are under the key named database , and add the `base64` encrypted password in `MYSQL_PASSWORD` key loacted under `secretEnv` key.)

4. Install the Helm chart:
    ```bash
    helm install leyline-assignment ./
    ```

5. To upgrade the deployment after making changes:
    ```bash
    helm upgrade leyline-assignment ./
    ```

6. To uninstall the deployment:
    ```bash
    helm uninstall leyline-assignment
    ```

7. To check the status of the deployment:
    ```bash
    helm status leyline-assignment
    ```

8. To see all the resources created by the Helm chart:
    ```bash
    kubectl get all -l app.kubernetes.io/instance=leyline-assignment
    ```

Note: Make sure your Kubernetes cluster has access to pull the Docker image specified in the `values.yaml` file. If you're using a private Docker registry, you may need to set up image pull secrets.

### Running Locally

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. create a `.env` file in the root directory with the following values:
   ```
    MYSQL_HOST="your host ip or address" # default localhost
    MYSQL_USER="your user" # default root
    MYSQL_PASSWORD="your password" # default is null
    MYSQL_DB="your db name" # default leyline_db
   ```
   **Note**:  these have default values assigned to them that are specified in the code if you want to use them just set up environment variable or specify the **MYSQL_PASSWORD** in `.env` file with correct password for database

3. Start the application:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 3000
    ```

## Directory structure

Below is the structure of the directory for a better understanding:
```
├── conftest.py
├── Dockerfile
├── docker-compose.yaml
├── Readme.md
├── .gitignore
├── app
│   ├── database.py
│   ├── main.py
│   └── routers
│       ├── health.py
│       ├── history.py
│       ├── lookup.py
│       └── validate.py
├── leyline-assignment-chart/
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