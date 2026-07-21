resource "kubernetes_namespace" "homework" {
  metadata {
    name = var.namespace
  }
}

resource "helm_release" "homework" {
  name       = "homework"
  chart      = "../helm"
  namespace  = kubernetes_namespace.homework.metadata[0].name

  set = [
    {
        name  = "image.repository"
        value = var.image_repository
    },
    {
        name  = "image.tag"
        value = var.image_tag
    },
    {
        name  = "environment"
        value = var.environment
    }
  ]
}