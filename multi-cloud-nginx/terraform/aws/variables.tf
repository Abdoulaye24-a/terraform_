# variables.tf - Bonne configuration

variable "aws_access_key" {
  description = "AWS Access Key"
  type        = string
  default     = "" # Utilisera les variables d'environnement AWS_ACCESS_KEY_ID si vide
}

variable "aws_secret_key" {
  description = "AWS Secret Key"
  type        = string
  sensitive   = true
  default     = "" # Utilisera les variables d'environnement AWS_SECRET_ACCESS_KEY si vide
}

variable "aws_key_name" {
  description = "AWS Key Pair Name"
  type        = string
  default     = "" # Doit être vide pour utiliser la clé SSH stockée dans les secrets GitHub
}
