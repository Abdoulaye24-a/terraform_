provider "aws" {
  region = "us-east-1"
  # Pas besoin de définir access_key / secret_key ici
  # Terraform les prendra dans les variables d’environnement GitHub Actions
}

resource "aws_instance" "vm" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t2.micro"
  key_name      = var.aws_key_name

  tags = {
    Name = "vm-aws-nginx"
  }
}
