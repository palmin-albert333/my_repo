output "external_ip_address_app" {
  value = module.app.external_ip_address_app
}

resource "local_file" "AnsibleInventory" {
 content = templatefile("inventory.json",
 {
  external_ip_address_app = module.app.external_ip_address_app,
 }
 )
 filename = "../../ansible/environments/stage/inventory.json"
}
