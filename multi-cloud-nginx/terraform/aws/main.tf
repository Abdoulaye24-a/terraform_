provider "aws" {
  region = "eu-north-1"
}

# Security Group pour autoriser HTTP et SSH
resource "aws_security_group" "nginx_sg" {
  name_prefix = "nginx-sg-"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "nginx-security-group"
  }
}

resource "aws_instance" "vm" {
  ami                    = "ami-0fe8bec493a81c7da"  # Ubuntu 22.04 en eu-north-1
  instance_type          = "t3.micro"
  key_name              = var.aws_key_name
  vpc_security_group_ids = [aws_security_group.nginx_sg.id]
  
  # S'assurer que l'instance a une IP publique
  associate_public_ip_address = true

  tags = {
    Name = "vm-aws-nginx"
  }
}
