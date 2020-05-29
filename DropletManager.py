import digitalocean
import time


class DropletManager:

    def __init__(self, api_token):
        self.regions = ["NYC1", "NYC3", "AMS3", "SFO2", "SFO3", "SGP1", "LON1", "FRA1", "TOR1", "BLR1"]
        self.manager = digitalocean.Manager(token=api_token)
        self.Droplet = digitalocean.Droplet
        self.ip = 0

    # def import_cloud_init(self):
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

    def create_server(self, region):
        self.Droplet = digitalocean.Droplet(token=self.manager.token, name='VPNdroplet', region=region.lower(), image='ubuntu-20-04-x64', size_slug='s-1vcpu-1gb', user_data="")
        self.Droplet.create()
        time.sleep(30)
        self.ip = self.Droplet.load().ip_address

    def delete_server(self):
        self.Droplet.destroy()
        print("Droplet Destroyed")
