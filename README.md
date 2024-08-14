# openapi-to-uptime-kuma

openapi-to-uptime-kuma is a Python tool designed to automate the registration of monitoring URLs into Uptime-Kuma, a self-hosted monitoring tool. This tool parses an OpenAPI specification file, extracts example URLs, and registers them as monitoring targets in Uptime-Kuma via its API.


## Installation

Install the required dependencies:
```
pip install -r requirements.txt
```


## Configuration

- Copy the .env.example file to create a .env file:
```
cp .env.example .env
```

- Edit the .env file to set up your environment.


## Usage

To run the tool, use the following command:
```
python -m openapi_to_uptime_kuma --spec spec.yaml --service service1
```

### Arguments

- --spec: The path to the OpenAPI specification file (e.g., spec.yaml).
- --service: The name of the service which is used as a prefix and a status page ID.
