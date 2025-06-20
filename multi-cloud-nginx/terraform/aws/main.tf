provider "aws" {
  region = "eu-north-1"  # Changement de région
}

resource "aws_instance" "vm" {
  ami           = "ami-0fe8bec493a81c7da"  # Ubuntu 22.04 en eu-north-1
  instance_type = "t3.micro"               # Type disponible dans eu-north-1
  key_name      = var.aws_key_name

  tags = {
    Name = "vm-aws-nginx"
  }
}
