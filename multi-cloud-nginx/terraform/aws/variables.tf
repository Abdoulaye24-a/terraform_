# variables.tf - Bonne configuration
variable "aws_access_key" {
  description = "AWS Access Key"
  type        = string
  default     = "" # Utilisera les variables d'environnement
}

variable "aws_secret_key" {
  description = "AWS Secret Key"
  type        = string
  sensitive   = true
  default     = "" # Utilisera les variables d'environnement
}

variable "aws_key_name" {
  description = "AWS Key Pair Name"
  type        = string
  default     = "" # Doit être vide pour utiliser le secret GitHub
}
