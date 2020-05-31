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

    def import_cloud_init(self):
        with open("cloud_config.yml", 'r') as file:
            self.user_data = file.read().replace("\n", ' ')

    def print_account_info(self):
        print("Account Info: ")
        print("Email", self.manager.get_account().email)
        print("Account Status: ", self.manager.get_account().status)

    def check_credentials(self):
        try:  # Could be a better way
            if self.manager.get_account().status == "active":
                print("API Key is valid and Account is Active\n")
                return True
            else:
                print("Account Status is inactive")
                return False
        except:
            print("API Key is invalid")
            return False

    def create_server(self, regionChoice):
        self.Droplet = digitalocean.Droplet(token=self.manager.token,
                                            name='VPNdroplet',
                                            region=self.regions[regionChoice],
                                            image='ubuntu-20-04-x64',
                                            size_slug='s-1vcpu-1gb',
                                            user_data=self.user_data)
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
