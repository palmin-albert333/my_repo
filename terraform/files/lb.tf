resource "yandex_lb_target_group" "reddit-app-target-group" {
  name = "reddit-app-target-group"

  dynamic "target" {
    for_each = yandex_compute_instance.app
    content {
      address   = target.value.network_interface.0.ip_address
      subnet_id = target.value.network_interface.0.subnet_id
    }
  }
}

resource "yandex_lb_network_load_balancer" "reddit-app-lb" {
  name = "reddit-app-load-balancer"

  listener {
    name = "reddit-app-listener"
    port = 9292
    external_address_spec {
      ip_version = "ipv4"
    }
  }

  attached_target_group {
    target_group_id = yandex_lb_target_group.reddit-app-target-group.id

    healthcheck {
      name = "reddit-healthcheck"
      http_options {
        port = 9292
      }
    }
  }
}
