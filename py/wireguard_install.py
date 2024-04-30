import os
import subprocess
import shutil
import ipaddress
import sys
from random import randint

WG_CONFIG = "/etc/wireguard/wg0.conf"

def get_free_udp_port():
    while True:
        port = randint(2000, 65000)
        if not subprocess.run(['ss', '-lau', '|', 'grep', str(port)], stdout=subprocess.DEVNULL).returncode == 0:
            return port

def check_root():
    if os.geteuid() != 0:
        print("Sorry, you need to run this as root")
        sys.exit()

def check_tun_device():
    if not os.path.exists('/dev/net/tun'):
        print("The TUN device is not available. You need to enable TUN before running this script")
        sys.exit()

def check_distro():
    if not os.path.exists('/etc/centos-release'):
        print("Your distribution is not supported (yet)")
        sys.exit()

def check_virtualization():
    if subprocess.check_output('systemd-detect-virt').strip() == b'openvz':
        print("OpenVZ virtualization is not supported")
        sys.exit()

def setup_wireguard(interactive=True):
    if not os.path.isfile(WG_CONFIG):
        private_subnet = ipaddress.ip_network("10.9.0.0/24")
        gateway_address = str(private_subnet.network_address + 1)
        server_port = get_free_udp_port()

        # Install WireGuard if needed
        if subprocess.run(['yum', 'list', 'installed', 'wireguard']).returncode != 0:
            shutil.copy2('/path/to/wireguard.repo', '/etc/yum.repos.d/')
            subprocess.run(['yum', 'install', 'wireguard', 'qrencode', 'wireguard-tools', 'firewalld', '-y'])

        server_privkey = subprocess.check_output('wg genkey', shell=True).decode().strip()
        server_pubkey = subprocess.check_output(f'echo {server_privkey} | wg pubkey', shell=True).decode().strip()
        
        # Prepare the configuration
        os.makedirs(os.path.dirname(WG_CONFIG), exist_ok=True)
        with open(WG_CONFIG, 'w') as f:
            f.write(f"""[Interface]
Address = {gateway_address}/{private_subnet.prefixlen}
ListenPort = {server_port}
PrivateKey = {server_privkey}
SaveConfig = false
""")
        
        # Configure firewall
        subprocess.run(['systemctl', 'start', 'firewalld'])
        subprocess.run(['systemctl', 'enable', 'firewalld'])
        subprocess.run(['firewall-cmd', '--zone=public', '--add-port={}/udp'.format(server_port)])
        subprocess.run(['firewall-cmd', '--zone=public', '--add-port={}/udp'.format(server_port), '--permanent'])
        
        print(f"Server configured with address {gateway_address} on port {server_port}")
    else:
        print("WireGuard is already set up.")

if __name__ == "__main__":
    check_root()
    check_tun_device()
    check_distro()
    check_virtualization()
    setup_wireguard()
