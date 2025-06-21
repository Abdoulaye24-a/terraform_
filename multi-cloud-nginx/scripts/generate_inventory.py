import subprocess
import os
import sys

def get_aws_ip_from_terraform():
    try:
        # Accès au bon dossier Terraform AWS
        terraform_dir = os.path.join(os.path.dirname(__file__), '../terraform/aws')
        
        print("📦 Récupération de l'IP AWS depuis Terraform...")
        result = subprocess.run(
            ['terraform', 'output', '-raw', 'aws_public_ip'],
            cwd=terraform_dir,
            capture_output=True,
            text=True,
            check=True
        )
        
        aws_ip = result.stdout.strip()
        if not aws_ip or aws_ip == 'null':
            raise ValueError("❌ IP AWS vide ou null")
            
        print(f"✅ IP trouvée : {aws_ip}")
        return aws_ip
        
    except subprocess.CalledProcessError as e:
        print(f"Erreur Terraform : {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur générale : {e}")
        sys.exit(1)

def create_inventory_file(aws_ip):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    inventory_path = os.path.join(script_dir, '../ansible/inventory.ini')
    os.makedirs(os.path.dirname(inventory_path), exist_ok=True)

    content = f"""[aws]
{aws_ip} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/aws.pem

[aws:vars]
ansible_ssh_common_args='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
ansible_python_interpreter=/usr/bin/python3
"""
    with open(inventory_path, 'w') as f:
        f.write(content)

    print(f"✅ Fichier généré : {inventory_path}")
    return inventory_path

def main():
    aws_ip = get_aws_ip_from_terraform()
    create_inventory_file(aws_ip)

if __name__ == "__main__":
    main()
