variable "namespace" {
  type = string
}

variable "environment" {
  type = string
}

variable "image_repository" {
  type        = string
}

variable "image_tag" {
  type = string
}

variable "kube_config_path" {
  type        = string
  description = "Path to the kubeconfig file used by the kubernetes and helm providers"
  default     = "~/.kube/config"
}