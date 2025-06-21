#!/usr/bin/env python3

import subprocess
import os
import sys
import re

def validate_ip_address(ip):
    """Valide qu'une chaîne est une adresse IP valide"""
    ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.match(ip_pattern, ip) is not None

def get_aws_ip_from_terraform():
    """Obtient l'IP AWS directement depuis Terraform"""
    try:
        # Aller dans le répertoire parent (où se trouve les fichiers Terraform)
        terraform_dir = os.path.join(os.path.dirname(__file__), '..')
        
        print("Récupération de l'IP AWS depuis Terraform...")
        
        # Exécuter la commande terraform output
        result = subprocess.run(
            ['terraform', 'output', '-raw', 'aws_public_ip'],
            cwd=terraform_dir,
            capture_output=True,
            text=True,
            check=True
        )
        
        aws_ip = result.stdout.strip()
        
        if not aws_ip or aws_ip == 'null':
            raise ValueError("IP AWS vide ou null")
        
        # Nettoyer l'IP de tout caractère indésirable
        aws_ip = aws_ip.replace('\n', '').replace('\r', '').replace('\t', '').strip()
        
        # Valider que c'est bien une IP
        if not validate_ip_address(aws_ip):
            raise ValueError(f"Format d'IP invalide: '{aws_ip}'")
            
        print(f"IP AWS trouvée et validée: {aws_ip}")
        return aws_ip
        
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de terraform output: {e}")
        print(f"Erreur stderr: {e.stderr}")
        # Essayer d'afficher toutes les sorties disponibles
        try:
            all_outputs = subprocess.run(
                ['terraform', 'output'],
                cwd=terraform_dir,
                capture_output=True,
                text=True
            )
            print(f"Sorties Terraform disponibles:\n{all_outputs.stdout}")
        except:
            pass
        sys.exit(1)
    except Exception as e:
        print(f"Erreur: {e}")
        sys.exit(1)

def create_inventory_file(aws_ip):
    """Crée le fichier d'inventaire Ansible avec un format correct"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    inventory_path = os.path.join(script_dir, '../ansible/inventory.ini')
    
    # Créer le répertoire ansible s'il n'existe pas
    os.makedirs(os.path.dirname(inventory_path), exist_ok=True)
    
    # Format correct pour Ansible (pas de caractères spéciaux, espaces propres)
    inventory_content = f"""[aws_servers]
aws_server ansible_host={aws_ip} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/aws.pem

[aws_servers:vars]
ansible_ssh_common_args='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
ansible_python_interpreter=/usr/bin/python3
"""
    
    with open(inventory_path, 'w') as f:
        f.write(inventory_content)
    
    print(f"✓ Fichier d'inventaire créé: {inventory_path}")
    return inventory_path

def validate_inventory_file(inventory_path):
    """Valide le fichier d'inventaire créé"""
    try:
        # Tester le parsing du fichier d'inventaire avec ansible-inventory
        result = subprocess.run(
            ['ansible-inventory', '-i', inventory_path, '--list'],
            capture_output=True,
            text=True,
            check=True
        )
        print("✓ Fichier d'inventaire validé avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠ Erreur de validation de l'inventaire: {e}")
        print(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print("⚠ ansible-inventory non trouvé, validation ignorée")
        return True

def main():
    try:
        print("=== Génération de l'inventaire Ansible ===")
        
        # Obtenir l'IP AWS
        aws_ip = get_aws_ip_from_terraform()
        
        # Créer le fichier d'inventaire
        inventory_path = create_inventory_file(aws_ip)
        
        # Afficher le contenu créé
        print("\n=== Contenu du fichier d'inventaire ===")
        with open(inventory_path, 'r') as f:
            content = f.read()
            print(content)
        
        # Valider le fichier
        print("\n=== Validation du fichier ===")
        validate_inventory_file(inventory_path)
            
        print("\n✓ Génération de l'inventaire réussie!")
        print(f"✓ IP AWS: {aws_ip}")
        print(f"✓ Fichier: {inventory_path}")
        
    except Exception as e:
        print(f"✗ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
