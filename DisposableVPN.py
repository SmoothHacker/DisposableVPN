from DropletManager import DropletManager
import sys


def load_api_token():
    token_file = open("token.env")
    return token_file.read()


VPN_droplet = DropletManager(load_api_token())

if not VPN_droplet.check_credentials():
    print("Please check the token.env file")
    sys.exit(1)

while True:
    print(26 * "-", "DisposableVPN", 26 * "-")
    print("1. Create Droplet")
    print("2. Exit")
    print(67 * "-")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        print("Select Region")
        for x in VPN_droplet.regions:
            print(x, end=" ")

        regionChoice = input("Enter your region choice: ")
        VPN_droplet.create_server(regionChoice)
    elif choice == 2:
        print("Now Quitting .....")
        break
    else:
        input("Please Use numerical values. Enter any key to try again..")

    # Display status about server config

    while True:
        # Display menu about destroying server
        print("\n", 26 * "-", "DisposableVPN", 26 * "-")
        print("Droplet is Live! in ", regionChoice)
        print("External IP: ", VPN_droplet.ip, "\n")
        print("1. Destroy Droplet")
        print(67 * "-")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            VPN_droplet.delete_server()
            break
        else:
            input("Please Use numerical values. Enter any key to try again..")
