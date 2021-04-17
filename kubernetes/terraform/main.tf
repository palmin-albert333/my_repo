provider "yandex" {
  folder_id                = var.folder_id
}

resource "yandex_kms_symmetric_key" "key-a" {
  name              = "symetric-key"
  description       = "description for key"
  default_algorithm = "AES_128"
  rotation_period   = "8760h"
}
resource "yandex_kubernetes_cluster" "reddit_cluster_resource_name" {
  name        = "name"
  description = "description"
  network_id = var.network_id

  master {
    version = "1.15"
    zonal {
      subnet_id = var.subnet_id
      zone = "ru-central1-a"
    }

    public_ip = true

    maintenance_policy {
      auto_upgrade = true

    }
  }

  service_account_id      = var.service_account_key_id
  node_service_account_id = var.service_account_key_id


  release_channel = "STABLE"
  network_policy_provider = "CALICO"

  kms_provider {
    key_id = "${yandex_kms_symmetric_key.key-a.id}"
  }
}

resource "yandex_kubernetes_node_group" "my_node_group" {
  cluster_id  = "${yandex_kubernetes_cluster.reddit_cluster_resource_name.id}"
  name        = "name"
  description = "description"
  version     = "1.15"


  instance_template {
    platform_id = "standard-v2"
    nat         = true

    resources {
      memory = 8
      cores  = 4
    }

    boot_disk {
      type = "network-hdd"
      size = 150
    }

    scheduling_policy {
      preemptible = false
    }
  }

  scale_policy {
    fixed_scale {
      size = 2
    }
  }

  allocation_policy {
    location {
      zone = "ru-central1-a"
    }
  }

  maintenance_policy {
    auto_upgrade = true
    auto_repair  = true

  }
}

