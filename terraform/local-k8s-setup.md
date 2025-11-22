# Infrastructure as Code (IaC) - Local Kubernetes Setup

Due to the constraint of not having access to an Azure subscription, the deployment target has been shifted from Azure Kubernetes Service (AKS) to a **Local Kubernetes Cluster** (e.g., K3s, Minikube, or Kind).

This document serves as the replacement for the Terraform IaC, detailing the necessary steps for setting up the local cluster and documenting the trade-offs as required by the mission.

## 1. Local Cluster Setup (K3s/Minikube)

The following steps outline how to prepare a local cluster for deployment:

### Option A: K3s (Recommended for Production-like Local Testing)

K3s is a lightweight, certified Kubernetes distribution built for edge computing and local development.

1.  **Installation:**
    ```bash
    curl -sfL https://get.k3s.io | sh -
    ```
2.  **Get Kubeconfig:** The configuration file is typically located at `/etc/rancher/k3s/k3s.yaml`. Copy this file to `~/.kube/config` or use it directly.
3.  **Install Ingress Controller:** K3s comes with Traefik as a default Ingress Controller, which is sufficient for this setup.

### Option B: Minikube

Minikube is a tool that runs a single-node Kubernetes cluster inside a VM on your local machine.

1.  **Start Cluster:**
    ```bash
    minikube start
    ```
2.  **Enable Ingress:**
    ```bash
    minikube addons enable ingress
    ```

## 2. Deployment Trade-Offs (Local Cluster vs. Azure AKS)

The shift from a managed cloud service (AKS) to a local cluster (K3s/Minikube) introduces several significant trade-offs that must be documented:

| Feature | Azure AKS (Managed Cloud) | Local K3s/Minikube (Local Cluster) | Trade-Off / Impact |
| :--- | :--- | :--- | :--- |
| **Infrastructure Provisioning** | **Terraform** for full automation of VNet, Subnets, Load Balancers, and AKS control plane. | **Manual setup** (shell scripts/CLI) for the cluster itself. No cloud networking automation. | **Loss of IaC scope:** Terraform is now limited to *simulating* the cluster setup, not provisioning the underlying infrastructure. |
| **Control Plane Management** | **Fully Managed** by Azure. High availability, patching, and upgrades are handled automatically. | **Self-Managed.** User is responsible for cluster maintenance, upgrades, and ensuring uptime. | **Increased Operational Overhead:** Requires manual intervention for cluster health. |
| **Networking & Load Balancing** | **Azure Load Balancer** and **Azure CNI** for robust, scalable networking and external IP allocation. | **NodePort/HostPort** or a simple local Ingress Controller (Traefik/Nginx). External access is limited to the local machine. | **Limited Scalability & External Access:** Cannot handle production-level traffic or provide global access. |
| **Security & Compliance** | Integrated with **Azure AD, Key Vault, Azure Policy,** and robust RBAC. | Relies on **basic Kubernetes RBAC** and local machine security. No integrated cloud security services. | **Reduced Security Posture:** Missing enterprise-grade security features and compliance certifications. |
| **Cost** | Pay-as-you-go model. | Free (zero cost for the cluster itself). | **Cost Saving:** Excellent for development and testing environments. |

## 3. CI/CD Adaptation

The CI/CD pipeline (GitHub Actions) has been adapted to:

1.  **Remove Azure Login:** The `azure/login` step is no longer required.
2.  **Use Generic Kubeconfig:** The deployment step now relies on a Kubernetes Secret named `KUBE_CONFIG` (containing the base64 encoded kubeconfig file of the local cluster) to authenticate and deploy the Helm Chart. This makes the pipeline portable to any Kubernetes environment.
