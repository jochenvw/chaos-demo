#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Update the apt package index
sudo apt-get update

# Install packages needed to use the Kubernetes apt repository
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg

# Download the public signing key for the Kubernetes package repositories
sudo mkdir -p -m 755 /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.32/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
sudo chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg

# Add the Kubernetes apt repository
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.32/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo chmod 644 /etc/apt/sources.list.d/kubernetes.list

# Update apt package index again
sudo apt-get update

# Install kubectl
sudo apt-get install -y kubectl

# Verify the installation
kubectl version --client




# install Azure CLI + Azure Developer CLI
curl -fsSL https://aka.ms/install-azd.sh | bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash