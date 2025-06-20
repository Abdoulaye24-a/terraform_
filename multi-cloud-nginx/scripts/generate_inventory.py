import json

with open('multi-cloud-nginx/scripts/ips.json') as f:
    ips = json.load(f)

with open('multi-cloud-nginx/ansible/inventory.ini', 'w') as f:
    f.write('[all]\n')
    f.write(f"{ips['aws']} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/aws.pem\n")
