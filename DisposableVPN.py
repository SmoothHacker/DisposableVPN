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
    print("2. Regenerate Encryption Keys")
    print("3. Exit")
    print(67 * "-")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        print(26 * "-", "DisposableVPN", 26 * "-")
        print("Select Region")
        num = 1
        for x, region in VPN_droplet.regions.items():
            print("\t", x, ". ", region)
        print(67 * "-")
        regionChoice = input("Enter your region choice: ")
        VPN_droplet.create_server(regionChoice)
    elif choice == 2:
        print(26 * "-", "DisposableVPN", 26 * "-")
        print("Now Regenerating Encryption Keys . . . . .")
        VPN_droplet.generate_keys()
        print("\nNew Encryption Keys Generated and loaded")
        print(67 * "-")
    elif choice == 3:
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
