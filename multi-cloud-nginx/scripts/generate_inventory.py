#!/usr/bin/env python3

import subprocess
import os
import sys

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
            
        print(f"IP AWS trouvée: {aws_ip}")
        return aws_ip
        
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de terraform output: {e}")
        print(f"Erreur stderr: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur: {e}")
        sys.exit(1)

def create_inventory_file(aws_ip):
    """Crée le fichier d'inventaire Ansible"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    inventory_path = os.path.join(script_dir, '../ansible/inventory.ini')
    
    # Créer le répertoire ansible s'il n'existe pas
    os.makedirs(os.path.dirname(inventory_path), exist_ok=True)
    
    inventory_content = f"""[aws_servers]
{aws_ip} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/aws.pem

[aws_servers:vars]
ansible_ssh_common_args='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
ansible_python_interpreter=/usr/bin/python3
"""
    
    with open(inventory_path, 'w') as f:
        f.write(inventory_content)
    
    print(f"✓ Fichier d'inventaire créé: {inventory_path}")
    return inventory_path

def main():
    try:
        # Obtenir l'IP AWS
        aws_ip = get_aws_ip_from_terraform()
        
        # Créer le fichier d'inventaire
        inventory_path = create_inventory_file(aws_ip)
        
        # Afficher le contenu créé
        print("\nContenu du fichier d'inventaire:")
        with open(inventory_path, 'r') as f:
            print(f.read())
            
        print("✓ Génération de l'inventaire réussie!")
        
    except Exception as e:
        print(f"✗ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
