#!/bin/bash

apt update && apt install wireguard -y

echo '
  [Interface]
  PrivateKey = MFvqEvBGFemTX8WH2SDIUGidPZWueKhSaupPBrcTqFI=
  Address = 10.0.0.1/24
  ListenPort = 51820

  [Peer]
  PublicKey = t0nCldmMZphDNnRiPNA3Z/Er2S5gq2BGI5mdN97kyCE=
  AllowedIPs = 10.0.0.2/32
  ' > /etc/wireguard/wg0.conf

cd /etc/wireguard/
wg-quick up wg0.conf