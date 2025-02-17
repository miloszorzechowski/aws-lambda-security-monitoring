terraform {
  backend "s3" {
    bucket       = null
    key          = "terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
    profile      = null
  }
}
