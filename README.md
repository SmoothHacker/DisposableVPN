# DisposableVPN
A Python 3 app that creates a Wireguard endpoint in Digital Ocean

## Setup
1. Install The API client through `pip install -r requirements.txt`.
2. Place your Digital Ocean API key inside of `token.env` in the root of the project directory

## How to Use
The Wireguard config file is inside of the `keys/` directory as `wgVPN.conf`
Public and Private Keys are already generated. One the app tells you the server is live.
Open the Wireguard config file with your favorite client. This works for Linux, Windows, and Mac OSx
