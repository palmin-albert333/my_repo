output "external_ip" {
  value = yandex_kubernetes_cluster.reddit_cluster_resource_name.master[0].public_ip
}

