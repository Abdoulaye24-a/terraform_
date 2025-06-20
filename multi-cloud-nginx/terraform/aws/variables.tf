# variables.tf - Configuration pour AWS uniquement

variable "aws_access_key" {
  description = "AWS Access Key (optionnelle ici car injectée via GitHub Secrets)"
  type        = string
  default     = "" # Terraform utilisera AWS_ACCESS_KEY_ID si laissé vide
}

variable "aws_secret_key" {
  description = "AWS Secret Key (optionnelle ici car injectée via GitHub Secrets)"
  type        = string
  sensitive   = true
  default     = "" # Terraform utilisera AWS_SECRET_ACCESS_KEY si laissé vide
}

variable "aws_key_name" {
  description = "Nom de la paire de clés EC2 (ex: aws-key.pem sans l'extension)"
  type        = string
  default     = "" # À injecter via GitHub Secret TF_VAR_aws_key_name
}
