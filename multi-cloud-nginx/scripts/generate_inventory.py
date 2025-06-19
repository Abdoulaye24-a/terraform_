import json

with open('ips.json') as f:
    ips = json.load(f)

with open('ansible/inventory.ini', 'w') as f:
    f.write('[all]\n')
    f.write(f"{ips['aws']} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/aws.pem\n")
    f.write(f"{ips['azure']} ansible_user=azureuser ansible_ssh_private_key_file=~/.ssh/azure.pem\n")
    f.write(f"{ips['gcp']} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/gcp.pem\n")