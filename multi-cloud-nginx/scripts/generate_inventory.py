import json
import os
import sys
import re

def clean_json_content(content):
    """Remove control characters that might break JSON parsing"""
    # Remove control characters except for valid JSON whitespace
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', content)
    return cleaned.strip()

def parse_ips_file(file_path):
    """Parse the IPs file with error handling and cleaning"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # First attempt: parse as-is
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print("Initial JSON parsing failed, attempting to clean content...")
            
            # Second attempt: clean and parse
            cleaned_content = clean_json_content(content)
            try:
                return json.loads(cleaned_content)
            except json.JSONDecodeError as e:
                print(f"JSON parsing failed even after cleaning. Error: {e}")
                print(f"Content around error position: {repr(cleaned_content[max(0, e.pos-20):e.pos+20])}")
                raise
                
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        sys.exit(1)

def generate_inventory(ips_data, inventory_path):
    """Generate the Ansible inventory file"""
    if not isinstance(ips_data, dict):
        raise ValueError("IP data should be a dictionary")
    
    if 'aws' not in ips_data:
        raise KeyError("'aws' key not found in IP data")
    
    aws_ip = ips_data['aws'].strip()
    if not aws_ip:
        raise ValueError("AWS IP address is empty")
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(inventory_path), exist_ok=True)
    
    with open(inventory_path, 'w') as f:
        f.write('[aws_servers]\n')
        f.write(f"{aws_ip} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/aws.pem\n\n")
        f.write('[aws_servers:vars]\n')
        f.write("ansible_ssh_common_args='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'\n")
        f.write("ansible_python_interpreter=/usr/bin/python3\n")
    
    return aws_ip

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ips_path = os.path.join(script_dir, 'ips.json')
    inventory_path = os.path.join(script_dir, '../ansible/inventory.ini')
    
    try:
        # Parse the IPs file
        ips_data = parse_ips_file(ips_path)
        
        # Generate inventory
        aws_ip = generate_inventory(ips_data, inventory_path)
        
        print(f"✓ Successfully generated inventory file: {inventory_path}")
        print(f"✓ AWS IP: {aws_ip}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
