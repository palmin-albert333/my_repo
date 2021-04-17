#output "external_ip_address_app" {
#  value = yandex_compute_instance.app.network_interface.0.nat_ip_address
#}
#output "external_ip_address_db" {
#  value = yandex_compute_instance.db.network_interface.0.nat_ip_address
#}
output "external_ip_address_app" {
  value = module.app.external_ip_address_app
}
output "external_ip_address_db" {
  value = module.db.external_ip_address_db
}
