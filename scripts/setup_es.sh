#!/bin/bash

# Define variables
ELASTICSEARCH_VERSION=7.17.10
ES_DIR="../integrations/"
ES_PACKAGE="elasticsearch-${ELASTICSEARCH_VERSION}-linux-x86_64.tar.gz"

# Create the directory for extensions if it doesn't exist
mkdir -p ${ES_DIR}

# Function to install prerequisites
install_prerequisites() {
    echo "Installing prerequisites..."
    sudo apt update
    sudo apt install -y wget
}

# Function to download Elasticsearch
download_elasticsearch() {
    echo "Downloading Elasticsearch..."
    wget https://artifacts.elastic.co/downloads/elasticsearch/${ES_PACKAGE} -P ${ES_DIR}
}

# Function to extract Elasticsearch
extract_elasticsearch() {
    echo "Extracting Elasticsearch..."
    tar -xzf ${ES_DIR}/${ES_PACKAGE} -C ${ES_DIR}
    rm -rf ${ES_DIR}/${ES_PACKAGE}
    echo "Removed elasticsearch tar"
}

# Function to start Elasticsearch locally
start_elasticsearch() {
    echo "Starting Elasticsearch..."
    ${ES_DIR}/elasticsearch-${ELASTICSEARCH_VERSION}/bin/elasticsearch -d
    
    # Wait for Elasticsearch to start
    echo "Waiting for Elasticsearch to start..."
    sleep 240
}

# Function to check Elasticsearch status
check_elasticsearch_status() {
    echo "Checking Elasticsearch status..."
    curl -X GET "localhost:9200/?pretty"
}

# Main script execution
install_prerequisites
download_elasticsearch
extract_elasticsearch
start_elasticsearch
check_elasticsearch_status

echo "Elasticsearch ${ELASTICSEARCH_VERSION} installed and running in ${ES_DIR}!"
