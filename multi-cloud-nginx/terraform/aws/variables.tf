variable "aws_access_key" {
  description = "AWS Access Key"
  type        = string
  default     = "" # Utilisera les variables d'environnement si vide
}

variable "aws_secret_key" {
  description = "AWS Secret Key"
  type        = string
  sensitive   = true
  default     = "" # Utilisera les variables d'environnement si vide
}

variable "aws_key_name" {
  description = "AWS Key Pair Name"
  type        = string
  default     = "your-default-key-name" # Remplace par ta clé SSH AWS ou laisse vide
}
