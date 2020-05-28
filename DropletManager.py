import digitalocean


class DropletManager:

    def __init__(self, api_token):
        self.manager = digitalocean.Manager(token=api_token)
        self.Droplet = digitalocean.Droplet

    # def import_cloud_init(self):
    def print_account_info(self):
        print("Account Info: ")
        print("Email", self.manager.get_account().email)
        print("Account Status: ", self.manager.get_account().status)

    def check_credentials(self):
        try: # Could be a better way
            if self.manager.get_account().status == "Active":
                print("API Key is valid and Account is Active")
                return True
            else:
                print("Account Status is inactive")
                return False
        except:
            print("API Key is invalid")
            return False

    #def create_server(self):

    #def delete_server(self):
