#!/bin/bash

# Define variables
ELASTICSEARCH_VERSION=7.17.10
ES_DIR="../integrations/"
ES_PACKAGE="elasticsearch-${ELASTICSEARCH_VERSION}-linux-x86_64.tar.gz"

# Source the .env file from the project root to access environment variables
# This assumes the .env file is located at ../.env relative to the script location
source ../.env

# Use the port from the .env file (defaulting to 9200 if not set)
ES_PORT=${ES_PORT:-9200}

# Create the directory for integrations if it doesn't exist
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
    echo "Removed Elasticsearch tar"
}

# Function to start Elasticsearch locally
start_elasticsearch() {
    echo "Starting Elasticsearch on port ${ES_PORT}..."
    ${ES_DIR}/elasticsearch-${ELASTICSEARCH_VERSION}/bin/elasticsearch -d -p ${ES_PORT}
    
    # Wait for Elasticsearch to start
    echo "Waiting for Elasticsearch to start..."
}

# Function to check if any Elasticsearch is already installed
check_existing_installation() {
    if [ -d "${ES_DIR}" ] && ls ${ES_DIR} | grep -q "elasticsearch-"; then
        echo "An existing Elasticsearch installation is detected in ${ES_DIR}:"
        ls ${ES_DIR} | grep "elasticsearch-"
        
        # Prompt the user to confirm if they want to overwrite
        read -p "Do you want to overwrite the existing installation? (y/n): " confirm
        if [ "$confirm" != "y" ]; then
            echo "Skipping Elasticsearch installation."
            start_elasticsearch
            exit 0
        else
            echo "Proceeding with the installation..."
        fi
    fi
}

# Function to check Elasticsearch status
check_elasticsearch_status() {
    echo "Checking Elasticsearch status..."
    curl -X GET "localhost:${ES_PORT}/?pretty"
}

# Main script execution
check_existing_installation  # Check for existing Elasticsearch installation
install_prerequisites
download_elasticsearch
extract_elasticsearch
start_elasticsearch
check_elasticsearch_status

echo "Elasticsearch ${ELASTICSEARCH_VERSION} installed and running in ${ES_DIR} on port ${ES_PORT}!"
