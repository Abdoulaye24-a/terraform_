provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project_id
  region      = "us-central1"
  zone        = "us-central1-a"
}

resource "google_compute_instance" "vm" {
  name         = "vm-gcp-nginx"
  machine_type = "e2-micro"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }

  metadata = {
    ssh-keys = "ubuntu:${file(var.public_key_path)}"
  }
}

output "gcp_public_ip" {
  value = google_compute_instance.vm.network_interface[0].access_config[0].nat_ip
}