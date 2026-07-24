terraform {
  required_version = ">= 1.5"
}

provider "kubernetes" {
    config_path = var.kube_config_path
}

provider "helm" {
    kubernetes = {
        config_path = var.kube_config_path
    }
}