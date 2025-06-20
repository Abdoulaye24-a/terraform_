import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
ips_path = os.path.join(script_dir, 'ips.json')
inventory_path = os.path.join(script_dir, '../ansible/inventory.ini')

try:
    with open(ips_path) as f:
        ips = json.load(f)
    
    with open(inventory_path, 'w') as f:
        # Groupe d'hôtes
        f.write('[aws_servers]\n')
        f.write(f"{ips['aws']} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/aws.pem\n\n")

        # Variables associées au groupe
        f.write('[aws_servers:vars]\n')
        f.write("ansible_ssh_common_args='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'\n")
        f.write("ansible_python_interpreter=/usr/bin/python3\n")

except FileNotFoundError:
    print(f"Error: File {ips_path} not found")
    exit(1)
except KeyError:
    print("Error: 'aws' key not found in ips.json")
    exit(1)
