# ElasticSearch
This application essentially functions as a miniature, internal version of Google Search for your own documents. It leverages Elasticsearch, a powerful open-source search and analytics engine, to index, search, and manage textual documents.

**Tested on:**
- **OS**: macOS 14.2.1
- **Python**: 3.12.1
- **Hardware**: Apple M1 with 16GB of RAM
  
&nbsp;

## Requirements

### Manual Installation
If you prefer to manually install packages, here is the list of packages which you can install:
```
- elasticsearch==7.13.3
- openai==1.9.0
- fastapi==0.109.2
- uvicorn==0.20.0
- pydantic==1.10.12
```

### Conda Installation
Open your terminal or command prompt and navigate to the directory containing the ```requirements.txt``` file. Run the following command to create a new [Conda](https://www.anaconda.com/download) environment. Replace <env_name> with your desired environment name:
```
conda create --name <env_name> --file requirements.txt
```
This command will attempt to create a new Conda environment with the name you specified and install all the packages listed in requirements.txt. Note that the platform specified in my requirements file is osx-64, which means this file is intended for my macOS systems. If you are using a different platform (e.g., Linux or Windows), you may need to adjust the package versions or names accordingly.

&nbsp;

## Running Elasticsearch and Kibana with Docker Compose
Before proceeding, ensure you have [Docker](https://www.docker.com/products/docker-desktop) installed.

### Docker Compose File
The ```docker-compose.yml``` file defines the services required to run Elasticsearch and Kibana.

### Running the Services
To launch both Elasticsearch and Kibana, follow these steps:

1. Navigate to the Directory: Ensure your terminal or command prompt is opened in the directory containing the docker-compose.yml file.

2. Start Services: Run the following command to start the services in detached mode:
```
docker-compose up -d
```
- The -d flag runs the containers in the background, allowing you to continue using the terminal.

## Understanding the Configuration
**Elasticsearch Service:** This service uses the official Elasticsearch image version 7.10.2. It's configured to run as a single-node cluster, suitable for development or lightweight production usage. The service exposes ports 9200 (HTTP) and 9300 (transport) for Elasticsearch.

**Kibana Service:** This service uses the official Kibana image version 7.10.2, which is designed to work seamlessly with the specified Elasticsearch version. Kibana is accessible via port 5601. It depends on the Elasticsearch service, ensuring Elasticsearch is launched first.

**Volumes:** A Docker volume named esdata is mounted to /usr/share/elasticsearch/data in the Elasticsearch container. This setup persists the Elasticsearch data, making it resilient across container restarts.

### Accessing Kibana
Once the services are running, you can access Kibana by navigating to http://localhost:5601 in your web browser. Kibana provides a user-friendly interface to interact with the Elasticsearch data.

### Stopping the Services
To stop the services and remove the containers, use the following command:
```
docker-compose down
```
- Optionally, to remove the data volume and clean up all data, add the -v flag at the end.

&nbsp;

## Run Your Application with Uvicorn
To start your FastAPI application with live reloading enabled, open your terminal or command prompt, navigate to the directory containing your main.py file, and run the following command:
```
uvicorn main:app --reload
```
Here, ```main``` is the name of your Python file (main.py) without the extension, and app is the name of the FastAPI instance. The ```--reload``` option makes the server restart upon code changes, which is very useful during development.

### API documentation (SwaggerUI)
Once Uvicorn is running, it will display the address where your app is being served, usually http://127.0.0.1:8000. FastAPI generates interactive API documentation using Swagger UI accessible at /docs on your application's root URL. To access it, go to:
```
http://127.0.0.1:8000/docs
```
