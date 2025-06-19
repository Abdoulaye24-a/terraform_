provider "aws" {
  region     = "us-east-1"
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

resource "aws_instance" "vm" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t2.micro"
  key_name      = var.aws_key_name != "" ? var.aws_key_name : null

  tags = {
    Name = "vm-aws-nginx"
  }
}
