import digitalocean
import time
import os


class DropletManager:

    def __init__(self, api_token):
        self.publickey_client = open(os.path.join(os.getcwd(), "keys", "publickey_client")).read()
        self.publickey_server = open(os.path.join(os.getcwd(), "keys", "publickey_server")).read()
        self.privatekey_client = open(os.path.join(os.getcwd(), "keys", "privatekey_client")).read()
        self.privatekey_server = open(os.path.join(os.getcwd(), "keys", "privatekey_server")).read()
        self.regions = {1: "NYC1", 2: "NYC3", 3: "AMS3", 4: "SFO2", 5: "SFO3", 6: "SGP1", 7: "LON1", 8: "FRA1", 9: "TOR1", 10: "BLR1"}
        self.manager = digitalocean.Manager(token=api_token)
        self.Droplet = digitalocean.Droplet
        self.ip = None
        self.user_data = None
        # Will be added via a generation function
        self.ssh_pub_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC6tkXKWck9CbTRDBVPKDNHqktSfDI05tInttlupUfd0difQM8mMZ36/gyQE3XZlyXv7YomN/ErSJB8LovqWms44FxY6JCKolgvSeUG/2f3pq08hTcZ1qdtp7MYI0C/t8aseP+0zinepMNaRw1Ta60h2Q+4gDQD2a/dFWbaYGPVruTvmEz5P9wVoIVWiGyDM52NE1fALLktOoRWgP12AimxcAtw8Dt5Exr+0alNXY4hBSpxpPf442Fal61BxSr3Xr6zdb5X2vpcvKuiUSww7GVv5q8fpJT9kUq5+XZdmJEvVCLdWe667PI6re/ClTekTOQZsj0Cb8Dr4XXzcU9zawzsHE4+CnKQKwDmWIz2FMAS7rqp+r2v+Umx1l+CNzXksKXtW/Px6j3kPuMVjZRxZ2ZcqAJdbbpqrN2FsNxwkOkp+4RxWmno4QNkj9hvgEjJx3aQgm6suh1Ajp6smGLbfAPh0LDNWTD9xSuk5ULYuIfguiPmxH4JXKRVO3f/LlGrZWs= DisposableVPN"
        if not self.manager.get_all_sshkeys().__contains__(self.ssh_pub_key):
            digitalocean.SSHKey(token=api_token, name="DisposableVPN", public_key=self.ssh_pub_key).create()

    def import_wireguard_script(self):
        with open("wireguard_setup.sh", 'r') as file:
            self.user_data = file.read().replace("\n", ' ')

    def print_account_info(self):
        print("Account Info: ")
        print("Email", self.manager.get_account().email)
        print("Account Status: ", self.manager.get_account().status)

    def check_credentials(self):
        try:  # Could be a better way
            if self.manager.get_account().status == "active":
                # Send SSH Key
                print("API Key is valid and Account is Active\n")
                return True
            else:
                print("Account Status is inactive")
                return False
        except:
            print("API Key is invalid")
            return False

    def create_server(self, region_choice):
        self.create_wireguard_configs()
        self.Droplet = digitalocean.Droplet(token=self.manager.token,
                                            name='VPNdroplet',
                                            region=self.regions[region_choice],
                                            image='ubuntu-20-04-x64',
                                            size_slug='s-1vcpu-1gb',
                                            user_data=self.user_data,
                                            ssh_key=self.ssh_pub_key)
        self.Droplet.create()
        time.sleep(20)
        self.ip = self.Droplet.load().ip_address

    def delete_server(self):
        self.Droplet.destroy()
        print("\nDroplet Destroyed\n")

    def generate_keys(self):
        os.system("cd keys/ && wg genkey | tee privatekey_server | wg pubkey > publickey_server")
        os.system("cd keys/ && wg genkey | tee privatekey_client | wg pubkey > publickey_client")
        self.publickey_client = open(os.path.join(os.getcwd(), "keys", "publickey_client")).read()
        self.publickey_server = open(os.path.join(os.getcwd(), "keys", "publickey_server")).read()
        self.privatekey_client = open(os.path.join(os.getcwd(), "keys", "privatekey_client")).read()
        self.privatekey_server = open(os.path.join(os.getcwd(), "keys", "privatekey_server")).read()

    def create_wireguard_configs(self):
        client_config_file = open("wg_client.conf", "w")
        client_config = f"""[Interface]
Address = 10.0.0.2/32
PrivateKey = {self.privatekey_client}
DNS = 1.1.1.1

[Peer]
PublicKey = {self.publickey_server}
Endpoint = {self.ip}:51820
AllowedIPs = 0.0.0.0/0
"""
        client_config_file.write(client_config)
        client_config_file.close()

        server_config_file = open("wireguard_setup.sh", "w")
        server_config = f"""#!/bin/bash
apt update && apt install wireguard -y
echo '
  [Interface]
  PrivateKey = {self.privatekey_server}
  Address = 10.0.0.1/24
  ListenPort = 51820

  [Peer]
  PublicKey = {self.publickey_client}
  AllowedIPs = 10.0.0.2/32
  ' > /etc/wireguard/wg0.conf
cd /etc/wireguard/
wg-quick up wg0.conf"""
        server_config_file.write(server_config)
        server_config_file.close()
