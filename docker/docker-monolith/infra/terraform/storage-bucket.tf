terraform {
  backend "s3" {
    endpoint   = "storage.yandexcloud.net"
    bucket     = "kipspm"
    region     = "ru-central-1"
    key        = "terraform.tfstate"
    access_key = "xxx"
    secret_key = "xxx"

    skip_region_validation      = true
    skip_credentials_validation = true
  }
}
