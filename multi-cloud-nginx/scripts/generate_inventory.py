#!/usr/bin/env python3

import os
import sys
import json

def get_aws_ip_from_file():
    """Obtient l'IP AWS depuis le fichier créé par Terraform"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ip_file = os.path.join(script_dir, 'ip.txt')
        
        if not os.path.exists(ip_file):
            raise FileNotFoundError(f"Fichier IP non trouvé: {ip_file}")
        
        with open(ip_file, 'r') as f:
            aws_ip = f.read().strip()
        
        if not aws_ip or aws_ip == 'null':
            raise ValueError("IP AWS vide ou null")
            
        print(f"IP AWS trouvée: {aws_ip}")
        return aws_ip
        
    except Exception as e:
        print(f"Erreur lors de la lecture de l'IP: {e}")
        sys.exit(1)

def create_inventory_file(aws_ip):
    """Crée le fichier d'inventaire Ansible"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Le script est dans multi-cloud-nginx/scripts/
    # L'inventaire doit être dans multi-cloud-nginx/ansible/
    inventory_path = os.path.join(script_dir, '..', 'ansible', 'inventory.ini')
    
    # Créer le répertoire ansible s'il n'existe pas
    os.makedirs(os.path.dirname(inventory_path), exist_ok=True)
    
    # Format d'inventaire compatible avec le playbook (hosts: aws)
    inventory_content = f"""[aws]
{aws_ip} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/aws.pem

[aws:vars]
ansible_ssh_common_args='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=30'
ansible_python_interpreter=/usr/bin/python3
ansible_ssh_timeout=30
"""
    
    with open(inventory_path, 'w') as f:
        f.write(inventory_content)
    
    print(f"✓ Fichier d'inventaire créé: {inventory_path}")
    return inventory_path

def validate_inventory_format(inventory_path):
    """Valide le format du fichier d'inventaire"""
    try:
        with open(inventory_path, 'r') as f:
            content = f.read()
            
        print("\n" + "="*50)
        print("CONTENU DE L'INVENTAIRE ANSIBLE")
        print("="*50)
        print(content)
        print("="*50)
        
        # Vérifications basiques
        if '[aws]' not in content:
            raise ValueError("Section [aws] manquante dans l'inventaire")
        
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        host_found = False
        
        for line in lines:
            if not line.startswith('[') and not line.startswith('#') and 'ansible_' not in line:
                host_found = True
                print(f"✓ Host trouvé: {line}")
        
        if not host_found:
            raise ValueError("Aucun host trouvé dans l'inventaire")
        
        print("✓ Format de l'inventaire validé avec succès")
        
    except Exception as e:
        print(f"✗ Erreur de validation de l'inventaire: {e}")
        sys.exit(1)

def create_backup_files():
    """Crée des fichiers de sauvegarde pour debug"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Lire l'IP
        with open(os.path.join(script_dir, 'ip.txt'), 'r') as f:
            ip = f.read().strip()
        
        # Créer un fichier de debug
        debug_info = {
            "aws_ip": ip,
            "timestamp": os.popen('date').read().strip(),
            "script_location": script_dir,
            "inventory_location": os.path.join(script_dir, '..', 'ansible', 'inventory.ini')
        }
        
        with open(os.path.join(script_dir, 'debug_info.json'), 'w') as f:
            json.dump(debug_info, f, indent=2)
        
        print("✓ Fichiers de debug créés")
        
    except Exception as e:
        print(f"Attention: Impossible de créer les fichiers de debug: {e}")

def main():
    try:
        print("="*60)
        print("GÉNÉRATION DE L'INVENTAIRE ANSIBLE")
        print("="*60)
        
        # Obtenir l'IP AWS depuis le fichier
        aws_ip = get_aws_ip_from_file()
        
        # Créer le fichier d'inventaire
        inventory_path = create_inventory_file(aws_ip)
        
        # Valider le format
        validate_inventory_format(inventory_path)
        
        # Créer des fichiers de debug
        create_backup_files()
        
        print("\n" + "="*60)
        print("✅ GÉNÉRATION DE L'INVENTAIRE RÉUSSIE!")
        print(f"📁 Fichier créé: {inventory_path}")
        print(f"🌐 IP AWS: {aws_ip}")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DE LA GÉNÉRATION: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
