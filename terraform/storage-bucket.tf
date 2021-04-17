terraform {
  backend "s3" {
    endpoint   = "storage.yandexcloud.net"
    bucket     = "terraform"
    region     = "ru-central1-a"
    key        = "terraform.tfstate"
    access_key = "accesskey"
    secret_key = "secretkey"

    skip_region_validation      = true
    skip_credentials_validation = true
  }
}
