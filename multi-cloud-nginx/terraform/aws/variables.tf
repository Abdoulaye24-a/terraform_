variable "aws_access_key" {
  description = "AWS Access Key"
  type        = string
  default     = "" # Laissez vide si vous passez par les variables d'environnement
}

variable "aws_secret_key" {
  description = "AWS Secret Key"
  type        = string
  sensitive   = true
  default     = "" # Laissez vide si vous passez par les variables d'environnement
}
