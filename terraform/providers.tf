terraform {
  required_version = ">= 1.5"
}

provider "kubernetes" {
    config_path = "/etc/rancher/k3s/k3s.yaml"
}

provider "helm" {
    kubernetes = {
        config_path = "/etc/rancher/k3s/k3s.yaml"
    }
}